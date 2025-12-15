from types import TracebackType
from typing import Self, cast

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.unit_of_work import UnitOfWork
from src.core.application.exceptions.unit_of_work_exceptions import (
    UnitOfWorkAlreadyCompletedError,
    UnitOfWorkAlreadyInitializedError,
    UnitOfWorkNotInitializedError,
)


class SQLAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, new_session: async_sessionmaker[AsyncSession]) -> None:
        self._new_session = new_session
        self._session: AsyncSession | None = None
        self._discarded = False
        self._transaction_completed = False

    def _register_repositories(self, session: AsyncSession) -> None:
        pass

    async def __aenter__(self) -> Self:
        self._check_not_initialized()
        self._session = self._new_session()
        self._register_repositories(self._session)
        return self

    async def __aexit__(
            self, 
            exc_type: type[BaseException] | None, 
            exc_val: BaseException | None, 
            exc_tb: TracebackType | None
        ) -> bool | None:
        if not self._transaction_completed:
            await self.rollback()

        await cast(AsyncSession, self._session).close()
        self._session = None

    async def commit(self) -> None:
        self._check_initialized()
        self._check_transaction_not_completed()
        # _check_initialized checks if the session is not None
        await cast(AsyncSession, self._session).commit()
        self._mark_transaction_completed()

    async def rollback(self) -> None:
        self._check_initialized()
        self._check_transaction_not_completed()
        # _check_initialized checks if the session is not None
        await cast(AsyncSession, self._session).rollback()
        self._mark_transaction_completed()

    def _check_initialized(self) -> None:
        if self._session is None:
            raise UnitOfWorkNotInitializedError(
                "Attempt to call unit of work methods outside context manager."
            )
        
    def _check_not_initialized(self) -> None:
        if self._session is not None:
            raise UnitOfWorkAlreadyInitializedError(
                "Attempt to initialize already initialized unit of work."
            )
        
    def _check_transaction_not_completed(self) -> None:
        if self._transaction_completed:
            raise UnitOfWorkAlreadyCompletedError(
                "Attempt to call .commit or .rollback methods second time in one context manager."
            )

    def _mark_transaction_completed(self) -> None:
        self._transaction_completed = True