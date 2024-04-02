from dataclasses import dataclass


@dataclass(slots=True)
class ProductMainData:
    title: str
    description: str
    brand: str
    sku: str
