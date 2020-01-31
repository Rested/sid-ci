package db

import (
	"context"
	"database/sql"
	"errors"
	"github.com/golang/protobuf/ptypes"
	"github.com/google/uuid"
	pb "github.com/sid-ci/server/pkg/gen"
	"golang.org/x/crypto/bcrypt"
	"log"
	"time"
)

type Token struct {
	ClientId   int
	ValidUntil time.Time
}

type Result struct {
	succeeded   bool
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
SELECT succeeded, received_at from sid_ci.results where job_uuid = ?;
`
	var result Result
	err := db.QueryRowContext(ctx, query, jobUuid).Scan(&result.succeeded, &result.receivedAt)
	if err != nil {
		return &pb.Job{}, err
	}
	statusAt, err := ptypes.TimestampProto(result.receivedAt)
	if err != nil {
		return &pb.Job{}, err
	}
	var status pb.Job_JobStatus
	if result.succeeded {
		status = pb.Job_FAILED
	} else {
		status = pb.Job_COMPLETED
	}
	return &pb.Job{
		JobStatus: status,
		JobUuid:   jobUuid,
		StatusAt:  statusAt,
	}, nil
}

func RecordHealthStatus(ctx context.Context, db sql.DB, healthStatus pb.HealthStatus) error {
	query := `
UPDATE sid_ci.clients SET 
	last_communication_at = ?,
	last_status = ?,
	active = ?
WHERE
	id = ?;
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
	query := "UPDATE sid_ci.clients set password = ? where identifier = ?"
	_, err = db.Exec(query, hashedPass, request.Identifier)
	if err != nil {
		return err
	}
	return nil
}

func Login(ctx context.Context, db sql.DB, request pb.LoginRequest) (*pb.Token, error) {
	var userPass string
	query := "select password from sid_ci.clients where identifier = ?"
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
