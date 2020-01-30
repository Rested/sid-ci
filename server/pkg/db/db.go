package db

import (
	"database/sql"
	"context"
	"github.com/golang/protobuf/ptypes"
	pb "github.com/sid-ci/server/pkg/gen"
	"time"
)

type Result struct {
	succeeded bool
	runEvents string
	imageDigest string
	gitHexSha string
	jobUuid string
	runBy int
	repo int
	receivedAt time.Time
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
		return  &pb.Job{}, err
	}
	var status pb.Job_JobStatus
	if result.succeeded {
		status = pb.Job_FAILED
	}else{
		status = pb.Job_COMPLETED
	}
	return &pb.Job{
		JobStatus: status,
		JobUuid:  jobUuid,
		StatusAt: statusAt,
	}, nil
}

func RecordHealthStatus(ctx context.Context, db sql.DB, healthStatus pb.HealthStatus) error {
	query := `
UPDATE sid.clients SET 
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
	_, err := db.Exec(query, ptypes.Timestamp(healthStatus.StatusAt), healthStatus.Status, active)
	if err != nil {
		return err
	}
	return nil
}