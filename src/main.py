import logging
from fastapi import FastAPI

from src.loader import Loader
from src.config import settings

__all__ = [
    "app",
]

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
)

loader = Loader()
app = FastAPI(lifespan=loader.lifespan)
