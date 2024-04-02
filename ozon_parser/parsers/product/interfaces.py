from collections.abc import Sequence
from typing import Protocol


class IProductMainData(Protocol):
    title: str
    description: str
    brand: str
    sku: str


class IProductMainDataParser(Protocol):
    def parse(self, html: str) -> IProductMainData: ...


class IProductCharacteristic(Protocol):
    name: str
    value: str


class IProductCharacteristicsParser(Protocol):
    def parse(self, html: str) -> Sequence[IProductCharacteristic]: ...


class IProductImagesParser(Protocol):
    def parse(self, html: str) -> Sequence[str]: ...
