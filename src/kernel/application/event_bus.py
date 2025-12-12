from abc import ABC, abstractmethod

from src.kernel.domain.domain_event import DomainEvent


class EventBus(ABC):
    
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None: ...

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"
    