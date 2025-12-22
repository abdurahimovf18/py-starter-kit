import pytest
from src.application.unit_of_work import UnitOfWork


@pytest.fixture
async def unit_of_work() -> UnitOfWork:

    async with UnitOfWork()
