import sys
from datetime import UTC
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pythonjsonlogger import jsonlogger

ROOT = Path(__file__).resolve().parent.parent.parent


class Env(BaseSettings):
    # System settings
    DEBUG: Literal["true", "false"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # Rabbitmq settings
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    # Redis settings
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: int

    model_config = SettingsConfigDict(
        env_file=ROOT / ".env"
    )


env = Env()  # type: ignore

# System settings
DEBUG: bool = env.DEBUG == "true"
TIMEZONE = UTC

# Postgresql settings
POSTGRES_USER = env.POSTGRES_USER 
POSTGRES_PASSWORD = env.POSTGRES_PASSWORD
POSTGRES_HOST = env.POSTGRES_HOST
POSTGRES_PORT = env.POSTGRES_PORT
POSTGRES_DB = env.POSTGRES_DB 

# Redis settings
RABBITMQ_USER = env.RABBITMQ_USER 
RABBITMQ_PASSWORD = env.RABBITMQ_PASSWORD
RABBITMQ_HOST = env.RABBITMQ_HOST
RABBITMQ_PORT = env.RABBITMQ_PORT

# Redis settings
REDIS_HOST = env.REDIS_HOST
REDIS_PORT = env.REDIS_PORT
REDIS_PASSWORD = env.REDIS_PASSWORD
REDIS_DB = env.REDIS_DB

# Logging settings
LOG_LEVEL = "DEBUG" if DEBUG else env.LOG_LEVEL 
LOG_DIRECTORY = ROOT / "resources" / "logs"

LOGGING_DICT_CONFIG: dict[str, object] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {
            "format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        },
        "json": { 
            "()": jsonlogger.JsonFormatter,  # type: ignore
            "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s:%(lineno)d",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain",
            "stream": sys.stdout,
            "level": LOG_LEVEL,
        },
        "json_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": LOG_DIRECTORY / "app.log.json",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
            "level": LOG_LEVEL,
        },
    },
    "root": {
        "handlers": ["console", "json_file"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "aiogram": {
            "handlers": ["console", "json_file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn": {
            "handlers": ["console", "json_file"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.access": {
            "handlers": ["console", "json_file"],
            "level": "INFO",
            "propagate": False
        },
        "fastapi": {
            "handlers": ["console", "json_file"],
            "level": "INFO",
            "propagate": False
        },
        "sqlalchemy.engine": {
            "handlers": ["console", "json_file"],
            "level": "WARNING",
            "propagate": False
        },
        "alembic": {
            "handlers": ["console", "json_file"],
            "level": "INFO",
            "propagate": False
        },
        "faststream": {
            "handlers": ["console", "json_file"],
            "level": "INFO",
            "propagate": False
        },
        "gunicorn": {
            "handlers": ["console", "json_file"],
            "level": "INFO",
            "propagate": False
        }
    }
}
