from typing import Annotated

from fastapi import Depends

from src.core import container


async def get_container() -> container.Container:
    raise NotImplementedError("Container dependency should be overriden!")

Container = Annotated[container.Container, Depends(get_container)]
