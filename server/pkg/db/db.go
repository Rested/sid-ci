package db

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"github.com/golang/protobuf/ptypes"
	"github.com/google/uuid"
	pb "github.com/sid-ci/server/pkg/gen"
	"golang.org/x/crypto/bcrypt"
	"log"
	"strings"
	"time"
)

type Token struct {
	ClientId   int
	ValidUntil time.Time
}

type Result struct {
	status      string
	runEvents   string
	imageDigest string
	gitHexSha   string
	jobUuid     string
	runBy       int
	repo        int
	receivedAt  time.Time
}

func GetJobStatus(ctx context.Context, db sql.DB, jobUuid string) (*pb.Job, error) {
	query := `
SELECT status, received_at from sid_ci.job where job_uuid = $1;
`
	var result Result
	err := db.QueryRowContext(ctx, query, jobUuid).Scan(&result.status, &result.receivedAt)
	if err != nil {
		return &pb.Job{}, err
	}
	statusAt, err := ptypes.TimestampProto(result.receivedAt)
	if err != nil {
		return &pb.Job{}, err
	}
	return &pb.Job{
		JobStatus: pb.Job_JobStatus(pb.Job_JobStatus_value[result.status]),
		StatusAt:  statusAt,
	}, nil
}

func RecordHealthStatus(ctx context.Context, db sql.DB, healthStatus pb.HealthStatus) error {
	query := `
UPDATE sid_ci.clients SET 
	last_communication_at = $1,
	last_status = $2,
	active = $3
WHERE
	id = $4;
`
	active := true
	if healthStatus.Status == pb.HealthStatus_INACTIVE {
		active = false
	}
	tokenInfo, ok := ctx.Value("tokenInfo").(Token)
	if !ok {
		return errors.New("no token info found")
	}
	healthAt, err := ptypes.Timestamp(healthStatus.StatusAt)
	_, err = db.Exec(query, healthAt, healthStatus.Status, active, tokenInfo.ClientId)
	if err != nil {
		return err
	}
	return nil
}

func hashAndSalt(pwd []byte) (string, error) {
	hash, err := bcrypt.GenerateFromPassword(pwd, bcrypt.MinCost*5)
	if err != nil {
		return "", err
	}
	return string(hash), nil
}
func comparePasswords(hashedPwd string, plainPwd []byte) bool { // Since we'll be getting the hashed password from the DB it
	// will be a string so we'll need to convert it to a byte slice
	byteHash := []byte(hashedPwd)
	err := bcrypt.CompareHashAndPassword(byteHash, plainPwd)
	if err != nil {
		log.Println(err)
		return false
	}

	return true
}

func ChangePass(ctx context.Context, db sql.DB, request pb.LoginRequest) error {
	_, err := Login(ctx, db, request)
	if err != nil {
		return err
	}
	bytesP := []byte(request.NewPassword)
	hashedPass, err := hashAndSalt(bytesP)
	if err != nil {
		return err
	}
	query := "UPDATE sid_ci.clients set password = $1 where identifier = $2"
	_, err = db.Exec(query, hashedPass, request.Identifier)
	if err != nil {
		return err
	}
	return nil
}

func Login(ctx context.Context, db sql.DB, request pb.LoginRequest) (*pb.Token, error) {
	var userPass string
	query := "select password from sid_ci.clients where identifier = $1"
	err := db.QueryRowContext(ctx, query, request.Identifier).Scan(&userPass)
	if err != nil {
		return &pb.Token{}, err
	}
	bytesP := []byte(request.Password)
	if comparePasswords(userPass, bytesP) {
		return &pb.Token{
			Token: uuid.New().String(),
		}, nil
	}
	return &pb.Token{}, errors.New("passwords did not match")

}

func ListReposMatching(ctx context.Context, db sql.DB, repo *pb.Repo) (retRepos []*pb.Repo, err error) {

	queryParts := make([]string, 0, 4)
	valueParts := make([]interface{}, 0, 4)
	queryParts = append(queryParts, "enabled = $1")
	valueParts = append(valueParts, repo.Enabled)

	if repo.AddedBy != 0 {
		queryParts = append(queryParts, "added_by = $2")
		valueParts = append(valueParts, repo.AddedBy)

	}
	if repo.Name != "" {
		valueParts = append(valueParts, repo.Name)
		queryParts = append(queryParts, fmt.Sprintf("name ~ $%d", len(queryParts)+1))
	}

	if repo.SshUrl != "" {
		valueParts = append(valueParts, repo.SshUrl)
		queryParts = append(queryParts, fmt.Sprintf("ssh_url ~ $%d", len(queryParts)+1))
	}

	query := fmt.Sprintf("select name, ssh_url, enabled, added_by from sid_ci.repos where %s", strings.Join(queryParts[:], " and "))
	rows, err := db.QueryContext(ctx, query, valueParts...)

	if err != nil {
		log.Fatal(err)
	}

	defer func() {
		if closeError := rows.Close(); closeError != nil {
			err = closeError
		}
	}()

	repos := make([]*pb.Repo, 0)
	for rows.Next() {
		var repo pb.Repo
		if err := rows.Scan(&repo.Name, &repo.SshUrl, &repo.Enabled, &repo.AddedBy); err != nil {
			// Check for a scan error.
			// Query rows will be closed with defer.
			log.Fatal(err)
		}
		repos = append(repos, &repo)
	}

	return repos, nil
}

func UpdateJob(ctx context.Context, db sql.DB, job *pb.Job) {
	query := `
insert into sid_ci.job (job_uuid, status, image_url, git_hexsha, repo_url)
	values ($1, $2, $3, $4, $5) on conflict (job_uuid) do update set 
		job_uuid = excluded.job_uuid,
		status = excluded.status,
	  	image_url = excluded.image_url,
	    git_hexsha = excluded.git_hexsha,
	   	repo_url = excluded.repo_url;
`
	_, err := db.QueryContext(ctx, query, job.JobUuid, job.JobStatus, job.ImageUrl, job.CommitHexsha, job.RepoSshUrl)
	if err != nil {
		log.Fatalf("Failed to upsert job %s: %v", job.JobUuid, err)
	}
	log.Printf("Upserted job %s", job.JobUuid)
}
