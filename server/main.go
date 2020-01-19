package main

import (
	"context"
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"sync"
	"time"

	"google.golang.org/grpc"

	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/testdata"

	"github.com/golang/protobuf/proto"

	pb "github.com/Rested/sid-ci/sid"
)

var (
	tls      = flag.Bool("tls", false, "Connection uses TLS if true, else plain TCP")
	certFile = flag.String("cert_file", "", "The TLS cert file")
	keyFile  = flag.String("key_file", "", "The TLS key file")
	port     = flag.Int("port", 10000, "The server port")
	host     = flag.String("host", "localhost", "The server host")
)

type sidServer struct {
	pb.UnimplementedSidServer
	// pb.UnimplementedRouteGuideServer
	// savedFeatures []*pb.Feature // read-only after initialized

	mu sync.Mutex // protects routeNotes
	// routeNotes map[string][]*pb.
}

// Get
func (s *sidServer) GetJob(ctx context.Context, healthStatus *pb.HealthStatus) (*pb.Job, error) {

	// No job was found, return an unnamed feature
	return &pb.Job{Location: point}, nil
}

// ListFeatures lists all features contained within the given bounding Rectangle.
func (s *sidServer) HealthStatusCheckIn(healthStatus *pb.HealthStatus, stream pb.Sid_HealthStatusCheckInServer) error {
	for _, feature := range s.savedFeatures {
		if inRange(feature.Location, rect) {
			if err := stream.Send(feature); err != nil {
				return err
			}
		}
	}
	return nil
}

// RecordRoute records a route composited of a sequence of points.
//
// It gets a stream of points, and responds with statistics about the "trip":
// number of points,  number of known features visited, total distance traveled, and
// total time spent.
func (s *sidServer) RecordJobRun(stream pb.Sid_RecordJobRunServer) error {
	var pointCount, featureCount, distance int32
	var lastPoint *pb.Point
	startTime := time.Now()
	for {
		point, err := stream.Recv()
		if err == io.EOF {
			endTime := time.Now()
			return stream.SendAndClose(&pb.RouteSummary{
				PointCount:   pointCount,
				FeatureCount: featureCount,
				Distance:     distance,
				ElapsedTime:  int32(endTime.Sub(startTime).Seconds()),
			})
		}
		if err != nil {
			return err
		}
		pointCount++
		for _, feature := range s.savedFeatures {
			if proto.Equal(feature.Location, point) {
				featureCount++
			}
		}
		if lastPoint != nil {
			distance += calcDistance(lastPoint, point)
		}
		lastPoint = point
	}
}

func newServer() *sidServer {
	s := &sidServer{} //routeNotes: make(map[string][]*pb.RouteNote)
	return s
}

func main() {
	flag.Parse()
	lis, err := net.Listen("tcp", fmt.Sprintf("%s:%d", *host, *port))
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
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
		opts = []grpc.ServerOption{grpc.Creds(creds)}
	}
	grpcServer := grpc.NewServer(opts...)
	pb.RegisterSidServer(grpcServer, newServer())
	grpcServer.Serve(lis)
}
