from collections.abc import Sequence
from dataclasses import dataclass

from ozon_parser.parsers.product.interfaces import IProductCharacteristic


@dataclass(slots=True)
class Product:
    sku: str
    name: str
    brand: str
    description: str
    characteristics: Sequence[IProductCharacteristic]
    images: Sequence[str]
