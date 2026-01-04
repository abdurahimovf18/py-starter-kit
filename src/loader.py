import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.application.event_bus import EventBus
from src.application.ports.clock import Clock
from src.application.ports.container import Container
from src.application.unit_of_work import UnitOfWork
from src.config import settings
from src.infrastructure.adapters.dict_container import DictContainer
from src.infrastructure.adapters.utc_clock import UTCClock
from src.infrastructure.rabbitmq_event_bus import RabbitMQEventBus
from src.infrastructure.sqlalchemy.setup import new_session
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.presentation import api

logger = logging.getLogger(__name__)


class Loader:
    def __init__(self):
        self.container: Container = DictContainer()
        logger.debug("Container created")

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncGenerator[None, None]:
        logger.info("FastAPI lifespan started")
        await self.setup_fastapi(app)
        await self.startup()
        yield
        await self.shutdown()
        logger.info("FastAPI lifespan completed")

    async def startup(self):
        logger.info("Application startup initialized")
        await self.setup_event_bus()
        await self.setup_unit_of_work()
        await self.setup_clock()
        logger.info("Application startup completed")

    async def shutdown(self):
        logger.info("Application cleanup initialized")
        await self.cleanup_event_bus()
        logger.info("Application cleanup completed")

    async def setup_fastapi(self, app: FastAPI) -> None:
        app.dependency_overrides[api.dependency_injection.get_container] = (
            self.get_container
        ) 
        logger.debug("FastAPI dependencies overriden")

        

        self.container.register_singleton(FastAPI, app)
        logger.debug("FastAPI registered")

    async def setup_event_bus(self) -> None:
        self.container.register_singleton(
            EventBus, 
            RabbitMQEventBus(
                self.container, 
                settings.RABBITMQ_USER, 
                settings.RABBITMQ_PASSWORD,
                settings.RABBITMQ_HOST,
                settings.RABBITMQ_PORT
            )
        )
        logger.debug(
            "EventBus registered",
            extra={"implementation": RabbitMQEventBus.__name__}
        )
        event_bus = await self.container.resolve(EventBus)
        await event_bus.start()
        logger.debug("EventBus started")

    async def cleanup_event_bus(self) -> None:
        event_bus = await self.container.resolve(EventBus)
        await event_bus.stop()
        logger.debug("EventBus stopped")

    async def setup_clock(self) -> None:
        self.container.register_singleton(Clock, UTCClock())
        logger.debug(
            "Clock registered",
            extra={"implementation": UTCClock.__name__}
        )

    async def setup_unit_of_work(self) -> None:
        self.container.register_sync_factory(
            UnitOfWork, 
            lambda: SQLAlchemyUnitOfWork(new_session)
        )
        logger.debug(
            "UnitOfWork registered",
            extra={"implementation": SQLAlchemyUnitOfWork.__name__}
        )

    async def get_container(self) -> Container:
        return self.container
    