from abc import ABC, abstractmethod
from typing import Self, Type
from types import TracebackType


class BaseUnitOfWork(ABC):

    @abstractmethod
    async def __aenter__(self) -> Self: ...
    
    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> bool | None:
        ...
    
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    def __repr__(self) -> str:
        return f"<{type(self).__name__}>"
    