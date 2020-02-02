import pydantic
import pathlib
from enum import Enum


class LogLevelEnum(Enum):
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


class Settings(pydantic.BaseSettings):
    poll_frequency_seconds: int = 60 * 5
    # postgres_dsn: pydantic.PostgresDsn
    # redis_dsn: pydantic.RedisDsn
    git_projects_path: pathlib.Path = pathlib.Path("/git-projects")
    db_timeout: int = 30
    redis_timeout: int = 30
    id_rsa_path: pydantic.FilePath  # used by git-exe.sh
    log_level: LogLevelEnum = LogLevelEnum.INFO
    abandonment_timeout: int = 60 * 10
    sid_server_dsn: pydantic.AnyUrl
    sid_server_timeout: int = 60
