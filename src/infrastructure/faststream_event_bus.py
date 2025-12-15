import logging
from collections.abc import Awaitable, Callable
from dataclasses import asdict
from typing import cast

from faststream import FastStream
from faststream.types import SendableMessage

from src.core.application.event_bus import EventBus
from src.core.application.exceptions.event_bus_exceptions import (
    EventBusAlreadyClosedError,
    EventBusAlreadyStartedError,
    EventBusNotStartedError,
    EventBusSetupError,
)
from src.core.container import Container
from src.core.domain.domain_event import DomainEvent

logger = logging.getLogger(__name__)


class FastStreamEventBus(EventBus):
    def __init__(self, app: FastStream) -> None:
        self._app = app
        self._broker = self._app.broker
        self._is_started = False

    async def start(self):
        if self._is_started:
            raise EventBusAlreadyStartedError(
                "Attempt to call .start method second time without closing."
            )
        self._is_started = True

        await self._app.start()

    async def close(self):
        if not self._is_started:
            raise EventBusAlreadyClosedError(
                "Attempt to call .close method second time without starting."
            )
        self._is_started = False

        await self._app.stop()

    async def publish(self, event: DomainEvent) -> None:
        if not self._is_started:
            raise EventBusNotStartedError(
                "Attempt to use event bus before starting it."
            )
        
        if self._broker is None:
            raise EventBusSetupError(
                "app.broker is not set. Broker must not be " 
                "BrokerUsecase[object, object] type, but got None"
            )
        
        event_data = cast(SendableMessage, asdict(event))
        await self._broker.publish(
            message=event_data, queue=event.event_name  # type: ignore
        )

    def subscribe(
            self, 
            event: DomainEvent, 
            handler: Callable[[DomainEvent, Container], Awaitable[None]]
        ) -> None:
        raise NotImplementedError("Subscribe method is not implemented")
