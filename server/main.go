package main

import (
	"context"
	"database/sql"
	"errors"
	"flag"
	"fmt"
	"github.com/caarlos0/env/v6"
	"github.com/go-redis/redis/v7"
	"github.com/golang/protobuf/ptypes"
	"github.com/grpc-ecosystem/go-grpc-middleware/auth"
	_ "github.com/lib/pq"
	dbapi "github.com/sid-ci/server/pkg/db"
	pb "github.com/sid-ci/server/pkg/gen"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/testdata"
	"io"
	"log"
	"net"
	"sync"
	"time"
)

var (
	tls       = flag.Bool("tls", false, "Connection uses TLS if true, else plain TCP")
	certFile  = flag.String("cert_file", "", "The TLS cert file")
	keyFile   = flag.String("key_file", "", "The TLS key file")
	port      = flag.Int("port", 10000, "The server port")
	host      = flag.String("host", "0.0.0.0", "The server host")
	redisDsn  = flag.String("redis_dsn", "", "The redis dsn, e.g redis://pass@host:6379")
	queueSize = flag.Int("queue_size", 100, "Number of jobs to queue at a time.")
)

type config struct {
	PostgresDsn string `env:"POSTGRES_DSN,required"`
}

var (
	tokenCache map[string]dbapi.Token
)

type sidServer struct {
	pb.UnimplementedSidServer
	// UnimplementedRouteGuideServer
	// savedFeatures []*Feature // read-only after initialized
	mu         sync.Mutex // protects routeNotes
	db         sql.DB
	red        redis.Client
	jobMap     map[string]pb.Job
	jobQueue   chan string
	jobStreams map[*pb.Sid_GetJobsServer]chan pb.Job
	// routeNotes map[string][]*
}

// Client wants a job, give it to them!
func (s *sidServer) GetJob(ctx context.Context, healthStatus *pb.HealthStatus) (*pb.Job, error) {
	// check fifo queue for a job
	select {
	case nextJobUUID := <-s.jobQueue:
		job := s.jobMap[nextJobUUID]
		pbJob := pb.Job{
			RepoName:     job.RepoName,
			RepoSshUrl:   job.RepoSshUrl,
			CommitHexsha: job.CommitHexsha,
			JobStatus:    pb.Job_BUILDING,
			StatusAt:     ptypes.TimestampNow(),
			JobUuid:      job.JobUuid,
		}
		// delete job from map
		delete(s.jobMap, nextJobUUID)
		// return job with updated time and status
		return &pbJob, nil
	default:
		return &pb.Job{StatusAt: ptypes.TimestampNow()}, nil
	}
}

func (s *sidServer) AddJob(ctx context.Context, job *pb.Job) (*pb.Job, error) {
	if val, ok := s.jobMap[job.JobUuid]; ok {
		return &val, nil
	}
	dbJob, err := dbapi.GetJobStatus(ctx, s.db, job.JobUuid)
	if err != nil || dbJob.JobStatus == pb.Job_ABANDONED {

		select {
		case s.jobQueue <- job.JobUuid:
			s.jobMap[job.JobUuid] = *job
			log.Printf("Successfully queued job: %s", job.JobUuid)
		default:
			log.Printf("Failed to queue job: %s.", job.JobUuid)
			if len(s.jobQueue) == cap(s.jobQueue) {
				log.Printf(`Capacity of jobQueue (%d) reached. Jobs will now be stored as abandonned in db. 
consider using a larger queue or adding more clients.`, cap(s.jobQueue))
			}
			job = &pb.Job{
				RepoName:     job.RepoName,
				RepoSshUrl:   job.RepoName,
				CommitHexsha: job.CommitHexsha,
				JobStatus:    pb.Job_ABANDONED,
				StatusAt:     ptypes.TimestampNow(),
				JobUuid:      job.JobUuid,
				ImageUrl:     job.ImageUrl,
			}
		}
		go dbapi.UpdateJob(context.Background(), s.db, job)
		for _, jobChan := range s.jobStreams {
			jobChan <- *job
		}


		return job, nil
	}
	return dbJob, nil
}

func (s *sidServer) Login(ctx context.Context, details *pb.LoginRequest) (*pb.Token, error) {
	// check if details match someone
	// if so return a token
	// otherwise return nothing
	return &pb.Token{}, errors.New("login failed")
}

func (s *sidServer) GetRepos(repo *pb.Repo, stream pb.Sid_GetReposServer) error {
	repos, err := dbapi.ListReposMatching(context.TODO(), s.db, repo)
	if err != nil {
		return err
	}
	for _, repo := range repos {
		if err = stream.Send(repo); err != nil {
			return err
		}
	}
	return nil
}

func (s *sidServer) GetJobs(repo *pb.Repo, stream pb.Sid_GetJobsServer) error {

	jobs, err := dbapi.ListJobsForRepo(stream.Context(), s.db, repo)
	if err != nil {
		return err
	}
	streamJobQueue := make(chan pb.Job, 10)
	s.jobStreams[&stream] = streamJobQueue

	for _, job := range jobs {
		if err = stream.Send(job); err != nil {
			return err
		}
	}
	// long running stream to client
	ctx := stream.Context()
	for {
		select {
		case job := <-s.jobStreams[&stream]:
			if err = stream.Send(&job); err != nil {
				log.Printf("Error sending new event. Deleting stream. Job streams length %d. %v", len(s.jobStreams), err)
				delete(s.jobStreams, &stream)
				return err
			}
		case <-ctx.Done():
			err = ctx.Err()
			if err == context.Canceled {
				log.Printf("Client cancelled, abandoning.")
			}
			log.Printf("Error sending new event. Deleting stream. Job streams length %d. %v", len(s.jobStreams), err)
			delete(s.jobStreams, &stream)
			return err
		}
	}
}

// ListFeatures lists all features contained within the given bounding Rectangle.
func (s *sidServer) HealthStatusCheckIn(stream pb.Sid_HealthStatusCheckInServer) error {
	for {
		healthStatus, err := stream.Recv()

		if err == io.EOF {
			// client disconnected
			go dbapi.RecordHealthStatus(context.Background(), s.db, pb.HealthStatus{
				Status:   pb.HealthStatus_INACTIVE,
				StatusAt: ptypes.TimestampNow(),
			})
			return stream.SendAndClose(&pb.CheckInResponse{
				Response: "Received",
			})
		}
		go dbapi.RecordHealthStatus(context.Background(), s.db, *healthStatus)
	}
}

// RecordJobRun accepts a stream of pb.JobRunEvents from the client
// These events are stored in the db asynchronously
func (s *sidServer) RecordJobRun(stream pb.Sid_RecordJobRunServer) error {
	for {
		jobEvent, err := stream.Recv()
		if jobEvent.Type == pb.JobRunEvent_ERROR {
			//updatedJob := pb.Job{
			//	RepoName:     jobEvent.Job.RepoName,
			//	RepoSshUrl:   jobEvent.Job.RepoSshUrl,
			//	CommitHexsha: jobEvent.Job.CommitHexsha,
			//	JobStatus:    pb.Job_FAILED,
			//	StatusAt:     jobEvent.EventAt,
			//}
			// record event async in db
			// change the job status to failed
		}
		if err == io.EOF {
			// check the last event was not a failure

			//
			//endTime := time.Now()
			return stream.SendAndClose(&pb.Job{})
		}
	}
}

func newServer() *sidServer {
	cfg := config{}
	if err := env.Parse(&cfg); err != nil {
		log.Fatalf("%+v\n", err)
	}
	log.Printf("cfg %s", cfg)
	log.Printf("Connecting to postgres on %s", cfg.PostgresDsn)
	db, err := sql.Open("postgres", cfg.PostgresDsn)

	//x := 1
	if err != nil {
		log.Fatalf("failed to connect to db %v", err)
	}
	//splitRedisDsn := strings.Split(redisDsn, "@")
	//splitAddrDb := strings.Split(splitRedisDsn[1], "/")
	//splitSchemePass := strings.Split(splitRedisDsn[0], "/")
	//redisDb := 0
	//if len(splitAddrDb) == 2 {
	//	redisDb, err = strconv.Atoi(splitAddrDb[1])
	//	if err != nil {
	//		log.Fatalf("Invalid redis db, could not convert db to an int: #{err}")
	//	}
	//}

	//red := redis.NewClient(&redis.Options{
	//	Addr:     splitAddrDb[0],
	//	Password: splitSchemePass[1],
	//	DB:       redisDb,
	//})
	//_, err = red.Ping().Result()
	//if err != nil {
	//	log.Fatalf("Failed to connect to redis: #{err}")
	//}
	queue := make(chan string, *queueSize)
	jobMap := make(map[string]pb.Job)
	jobStream := make(map[*pb.Sid_GetJobsServer]chan pb.Job, 0)
	s := &sidServer{db: *db, jobQueue: queue, jobMap: jobMap, jobStreams: jobStream} //routeNotes: make(map[string][]*RouteNote)
	return s
}

func authFunc(ctx context.Context) (context.Context, error) {
	token, err := grpc_auth.AuthFromMD(ctx, "bearer")
	if err != nil {
		return context.TODO(), err
	}
	if tokenInfo, ok := tokenCache[token]; ok {
		// check if token is expired
		if time.Now().After(tokenInfo.ValidUntil) {
			// remove the token
			delete(tokenCache, token)
			return context.TODO(), errors.New("expired token")
		}
		newCtx := context.WithValue(ctx, "tokenInfo", tokenInfo)
		return newCtx, nil
	}
	return context.TODO(), errors.New("token not found")
}

func main() {
	flag.Parse()
	lis, err := net.Listen("tcp", fmt.Sprintf("%s:%d", *host, *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	log.Printf("IM HERE 1")
	var opts []grpc.ServerOption
	if *tls {
		if *certFile == "" {
			*certFile = testdata.Path("server1.pem")
		}
		if *keyFile == "" {
			*keyFile = testdata.Path("server1.key")
		}
		creds, err := credentials.NewServerTLSFromFile(*certFile, *keyFile)
		if err != nil {
			log.Fatalf("Failed to generate credentials %v", err)
		}
		opts = []grpc.ServerOption{
			grpc.Creds(creds),
		}
	}
	//opts = append(
	//	opts,
	//	grpc.StreamInterceptor(grpc_auth.StreamServerInterceptor(authFunc)),
	//	grpc.UnaryInterceptor(grpc_auth.UnaryServerInterceptor(authFunc)))

	grpcServer := grpc.NewServer(
		opts...
	)

	pb.RegisterSidServer(grpcServer, newServer())

	log.Printf("Sid server listening on %s", fmt.Sprintf("%s:%d", *host, *port))
	grpcServer.Serve(lis)
}
