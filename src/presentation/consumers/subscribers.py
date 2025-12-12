import logging
from src.infrastructure.faststream.setup import broker

logger = logging.getLogger(__name__)


@broker.subscriber("undefined")
async def handle_undefined_message(data: dict[str, object]) -> None:
    logger.info("Event is skipped with event_name=undefined", extra=data)
    