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
    db_conn: psycopg2.extensions.connection,
):
    # add to fifo queue
    for repo in changed_repos:
        # check it is not already queued
        if any(
            status == STATUS_QUEUED
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
    redis_waiting_for = 0
    db_waiting_for = 0

    while True:
        logger.info("Attempting to poll and queue builds")
        cont = False
        try:
            db_conn = psycopg2.connect(settings.postgres_dsn)
        except psycopg2.Error:
            logger.debug("Failed to connect to db", exc_info=True)
            if db_waiting_for > settings.db_timeout:
                logger.error(
                    "Connection to Postgresql (%s) timed out after %d seconds",
                    settings.postgres_dsn,
                    settings.db_timeout,
                )
                break
            db_waiting_for += 1
            cont = True
        try:
            redis_conn = redis.Redis(
                host=settings.redis_dsn.host,
                port=settings.redis_dsn.port,
                db=settings.redis_dsn.path,
                password=settings.redis_dsn.password,
            )
        except redis.ConnectionError:
            logger.debug("Failed to connect to db", exc_info=True)
            if redis_waiting_for > settings.redis_timeout:
                logger.error(
                    "Connection to Redis (%s) timed out after %d seconds",
                    settings.redis_dsn,
                    settings.redis_timeout,
                )
                break
            redis_waiting_for += 1
            cont = True
        if cont:
            time.sleep(1)
            continue
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
