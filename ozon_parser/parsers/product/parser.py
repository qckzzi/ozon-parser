from collections.abc import Sequence

from ozon_parser.parsers.product.interfaces import (
    IProductCharacteristic,
    IProductCharacteristicsParser,
    IProductImagesParser,
    IProductMainData,
    IProductMainDataParser,
)
from ozon_parser.parsers.product.types import Product


class ProductParser:
    def __init__(
        self,
        main_data_parser: IProductMainDataParser,
        characteristics_parser: IProductCharacteristicsParser,
        images_parser: IProductImagesParser,
    ) -> None:
        self.main_data_parser: IProductMainDataParser = main_data_parser
        self.characteristics_parser: IProductCharacteristicsParser = characteristics_parser
        self.images_parser: IProductImagesParser = images_parser

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]"

    def parse(self, html: str) -> Product:
        main_data: IProductMainData = self.main_data_parser.parse(html)
        characteristics: Sequence[IProductCharacteristic] = self.characteristics_parser.parse(html)
        image_links: Sequence[str] = self.images_parser.parse(html)

        product: Product = Product(
            sku=main_data.sku,
            name=main_data.title,
            description=main_data.description,
            characteristics=characteristics,
            brand=main_data.brand,
            images=image_links,
        )

        return product
