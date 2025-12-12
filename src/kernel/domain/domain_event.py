import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Base class for domain events."""
    
    # Class-level constant — shared across all instances
    event_name: str = "undefined"
    
    # Auto-incrementing event ID (shared counter)
    _event_id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    _occured_at: datetime = field(default_factory=lambda: datetime.now(UTC), init=False)

    @property
    def event_id(self) -> uuid.UUID:
        return self._event_id

    @property
    def occured_at(self) -> datetime:
        return self._occured_at

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__} "
            f"event_name={self.event_name} "
            f"event_id={self._event_id} "
            f"occured_at={self._occured_at.isoformat()}>"
        )