import dataclasses
import time
import redis
import git
from settings import Settings
from typing import Optional, Tuple, List
from pathlib import Path
import psycopg2
import json
import logging
import sid_pb2_grpc
from google.protobuf.timestamp_pb2 import Timestamp
import sid_pb2
from uuid import uuid4
import grpc
import base64

settings = Settings()
logging.basicConfig(level=settings.log_level.value)

logger = logging.getLogger(__name__)

GIT_EXE_SCRIPT_LOCATION = Path.cwd().joinpath("git-exe.sh")


STATUS_QUEUED = "queued"
STATUS_BUILDING = "building"
STATUS_ABANDONED = "abandoned"


@dataclasses.dataclass
class Repository:
    name: str
    ssh_url: str
    enabled: bool
    target_ref: Optional[str] = None
    from_ref: Optional[str] = None
    status: str = "queued"
    status_at: Optional[time.time] = None

def get_enabled_repositories(
    db_conn: psycopg2.extensions.connection,
) -> Tuple[Repository]:
    with db_conn.cursor() as cursor:
        cursor.execute("select name, ssh_url from sid_ci.repos where enabled = true")
        return tuple(
            Repository(name=name, ssh_url=ssh_url, enabled=True)
            for name, ssh_url in cursor.fetchall()
        )


def check_for_changes_to_enabled_repos(repos: Tuple[Repository]) -> List[Repository]:
    changed_repos = []
    for repo in repos:
        local_repo_location = settings.git_projects_path.joinpath(repo.name)
        try:
            local_repo = git.Repo(path=local_repo_location)
            local_ref = local_repo.head.commit.tree.hexsha
            with local_repo.git.custom_environment(GIT_SSH=GIT_EXE_SCRIPT_LOCATION):
                target_ref = local_repo.remote().fetch()[0].commit.tree.hexsha
                local_repo.remote().pull()
            if local_ref == target_ref:
                logger.info("No changes detected in %s.", repo.name)
                continue
            logger.info(
                "Detected changes in %s from %s to %s", repo.name, local_ref, target_ref
            )
        except (git.exc.NoSuchPathError, git.exc.InvalidGitRepositoryError):
            local_repo = git.Repo.clone_from(
                url=repo.ssh_url,
                to_path=local_repo_location,
                env={"GIT_SSH": GIT_EXE_SCRIPT_LOCATION},
            )
            # TODO: use a specified branch
            target_ref = local_repo.head.commit.tree.hexsha
            logging.info("Successfully cloned new repo %s at %s", repo.name, target_ref)
            local_ref = None

        changed_repos.append(
            dataclasses.replace(repo, from_ref=local_ref, target_ref=target_ref,)
        )
    return changed_repos


def add_changed_repos_to_queue(
    changed_repos: Tuple[Repository],
    redis_conn: redis.Redis,
    stub: sid_pb2_grpc.SidStub
):
    # add to fifo queue
    for repo in changed_repos:
        # send to the server
        timestamp = Timestamp()

        stub.AddJob(sid_pb2.Job(
            repo_name=repo.name,
            repo_ssh_url=repo.ssh_url,
            commit_hexsha=repo.target_ref,
            job_status=sid_pb2.Job.JobStatus.QUEUED,
            status_at=timestamp.GetCurrentTime(),
            job_uuid=base64.b64encode(f"{repo.ssh_url}:{repo.target_ref}".encode("utf-8")).decode('utf-8')
        ))

        # check it is not already queued
        if any(
            status == sid_pb2.Job.JobStatus.QUEUED
            for status in redis_conn.hscan_iter(
                f"builds:{repo.name}:{repo.target_ref}", match="status",
            )
        ):
            logger.info("Already in queue: %s - %s", repo.name, repo.target_ref)
            continue
        # check it is not already building (if it is but is abandoned we can reque)
        building_task = redis_conn.hgetall(
            f"builds:{repo.name}:{repo.target_ref}"
        )
        if building_task:
            building_repo = Repository(**building_task)
            if (
                building_repo.status != STATUS_ABANDONED 
                and time.time() - building_repo.status_at
                < settings.abandonment_timeout
            ):
                logger.info(
                    "Already building (and not abandoned): %s - %s",
                    repo.name,
                    repo.target_ref,
                )
                continue
        # check it is not already built
        with db_conn.cursor() as cursor:
            cursor.execute(
                "SELECT git_hexsha from sid_ci.results where git_hexsha = %s;",
                (repo.target_ref,),
            )
            if cursor.fetchone():
                logger.info(
                    "Already got result in db for: %s - %s", repo.name, repo.target_ref
                )
                continue
        redis_conn.rpush("queue:builds", json.dumps(dataclasses.asdict(repo)))
        redis_conn.sadd("set:builds", f"{repo.name}@{repo.target_ref}")
        logger.info("Pushed changes redis queue for %s", repo.name)


def loop():
    server_waiting_for = 0

    while True:
        logger.info("Attempting to poll and queue builds")
        try:
            channel = grpc.insecure_channel(f"{settings.sid_server_dsn.host}:{settings.sid_server_dsn.port}")
            stub = sid_pb2_grpc.SidStub(channel)
        except grpc.RpcError:
            logger.debug("Failed to connect to server", exc_info=True)
            if server_waiting_for > settings.sid_server_timeout:
                logger.error("Connection to sid server (%s) timed out after %d seconds", settings.sid_server_dsn, settings.sid_server_timeout)
                break
            time.sleep(1)
        logger.info("Getting enabled repos")
        enabled_repos = get_enabled_repositories(db_conn)
        logger.info(
            "Enabled repos: \n%s",
            "\n".join([f"{r.name} - {r.ssh_url}" for r in enabled_repos]),
        )
        logger.info("Checking for changes in enabled repos")
        changed_repos = check_for_changes_to_enabled_repos(enabled_repos)
        add_changed_repos_to_queue(changed_repos, redis_conn, db_conn)
        logger.info(
            "Sleeping for %d seconds until next poll\n---",
            settings.poll_frequency_seconds,
        )
        time.sleep(settings.poll_frequency_seconds)
