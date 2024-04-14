from bs4 import BeautifulSoup, Tag

from ozon_parser.parsers.product_characteristic.types import Characteristic


class ProductCharacteristicsParser:
    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]"

    def parse(self, html: str) -> list[Characteristic]:
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        raw_characteristics: list[Tag] = soup.find(  # type: ignore[assignment, union-attr]
            "div",
            attrs={"id": "section-characteristics"},
        ).find_all(
            "dl",
        )

        characteristics: list[Characteristic] = []

        for raw_characteristic in raw_characteristics:
            tag_strings: list[str] = list(filter(lambda x: x not in (" ,", ", "), list(raw_characteristic.strings)))
            characteristics_real_count: int = len(tag_strings) - 1

            name: str = tag_strings[0]

            for i in range(characteristics_real_count):
                value: str = tag_strings[i + 1]

                if value == ": " or not value.strip():
                    continue

                characteristics.append(Characteristic(name=name, value=value))

        return characteristics
