from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream import FastStream

from src.application.ports.clock import Clock
from src.application.unit_of_work import UnitOfWork
from src.core.application.event_bus import EventBus
from src.core.container import Container
from src.infrastructure.adapters.utc_clock import UTCClock
from src.infrastructure.faststream.setup import faststream_app
from src.infrastructure.faststream_event_bus import FastStreamEventBus
from src.infrastructure.sqlalchemy.setup import new_session
from src.infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from src.presentation import api


class Loader:

    def __init__(self):
        self.container = Container()

    @asynccontextmanager
    async def lifespan(self, fastapi_app: FastAPI) -> AsyncGenerator[None, None]:
        self.container.register_singleton(FastAPI, fastapi_app)
        fastapi_app.include_router(api.routers.router)
        await self.startup()
        yield
        await self.shutdown()

    async def startup(self):
        await self.setup_core_dependencies()
        await self.setup_framework_dependencies()
        event_bus = await self.container.resolve(EventBus)
        await event_bus.start()

    async def shutdown(self):
        event_bus = await self.container.resolve(EventBus)
        await event_bus.close()

    async def setup_core_dependencies(self) -> None:
        self.container.register_singleton(EventBus, FastStreamEventBus(faststream_app))
        self.container.register_singleton(Clock, UTCClock())
        self.container.register_sync_factory(UnitOfWork, lambda: SQLAlchemyUnitOfWork(new_session))
    
    async def setup_framework_dependencies(self):
        self.container.register_singleton(FastStream, faststream_app)
        fastapi_app = await self.container.resolve(FastAPI)
        fastapi_app.dependency_overrides[api.dependency_injection.get_container] = (
            self.get_container
        ) 
    
    async def get_container(self) -> Container:
        return self.container
    