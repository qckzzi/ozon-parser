from collections.abc import Sequence
from typing import Any, Protocol, TypedDict


class ICharacteristic(TypedDict):
    name: str
    value: str


class IProduct(TypedDict):
    sku: str
    name: str
    brand: str
    description: str
    characteristics: Sequence[ICharacteristic]
    images: Sequence[str]


class IMQBroker(Protocol):
    async def publish(self, message: str, queue: str) -> Any: ...
