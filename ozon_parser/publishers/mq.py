import json

from ozon_parser.interfaces import ILogger
from ozon_parser.publishers.interfaces import IMQBroker, IProduct


class ParsedProductMQPublisher:
    def __init__(self, broker: IMQBroker, parsed_loading_queue: str) -> None:
        self.broker: IMQBroker = broker
        self.parsed_loading_queue: str = parsed_loading_queue

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]"

    async def publish(self, product: IProduct, logger: ILogger | None = None) -> None:
        await self.broker.publish(json.dumps(product), queue=self.parsed_loading_queue)
        logger.debug(f"{self} published '{product["name"]}' product")
