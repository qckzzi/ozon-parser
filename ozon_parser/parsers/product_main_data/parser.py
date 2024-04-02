import json

from bs4 import BeautifulSoup

from ozon_parser.parsers.product_main_data.types import ProductMainData


class ProductMainDataParser:
    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]"

    def parse(self, html: str) -> ProductMainData:
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        main_data: dict = json.loads(soup.find("script", attrs={"type": "application/ld+json"}).text)
        title: str = main_data["name"]
        description: str = main_data["description"]
        brand: str = main_data["brand"]
        sku: str = main_data["sku"]

        product_main_data: ProductMainData = ProductMainData(
            title=title,
            description=description,
            brand=brand,
            sku=sku,
        )

        return product_main_data
