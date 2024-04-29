from collections.abc import Sequence
from typing import Protocol, TypedDict

from ozon_parser.interfaces import ILogger


class ICharacteristic(Protocol):
    name: str
    value: str


class IProduct(Protocol):
    sku: str
    name: str
    brand: str
    description: str
    characteristics: Sequence[ICharacteristic]
    images: Sequence[str]


class IProductParser(Protocol):
    def parse(self, html: str) -> IProduct: ...


class IHtmlGetter(Protocol):
    def get_html(self, url: str, logger: ILogger | None = None) -> str: ...


class IPublishedCharacteristic(TypedDict):
    name: str
    value: str


class IPublishedProduct(TypedDict):
    sku: str
    name: str
    brand: str
    description: str
    characteristics: Sequence[IPublishedCharacteristic]
    images: Sequence[str]
    url: str


class IPublisher(Protocol):
    async def publish(self, product: IPublishedProduct, logger: ILogger | None = None) -> None: ...
