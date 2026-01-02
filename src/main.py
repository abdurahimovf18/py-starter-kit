"""
Application entry point.

This module exposes a single public variable `app`, which is the FastAPI
application instance.  External ASGI servers (Uvicorn, Gunicorn, etc.)
import this module to run the application.

All application bootstrapping is delegated to the Loader, which acts as
the composition root and manages application startup and shutdown.
"""

import logging
# Required so `logging.config.dictConfig` is available
import logging.config

from fastapi import FastAPI

from src.config import settings
from src.loader import Loader

# Only `app` is intended to be imported by external runners
__all__ = ["app"]

# Configuring logging module with dictConfig.
logging.config.dictConfig(settings.LOGGING_DICT_CONFIG)

# Create the FastAPI application instance.
app = FastAPI(lifespan=Loader().lifespan)
