import re
from collections.abc import Sequence
from typing import Final
from urllib.parse import ParseResult, urlparse, urlunparse

from bs4 import BeautifulSoup, ResultSet

from ozon_parser.exceptions import PagesCountNotFoundError
from ozon_parser.interfaces import ILogger
from ozon_parser.parsers.seller.interfaces import IHtmlGetter


class SellerParser:
    def __init__(self, html_getter: IHtmlGetter) -> None:
        self.html_getter: Final[IHtmlGetter] = html_getter

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]"

    async def parse(self, url: str, logger: ILogger | None = None) -> Sequence[str]:
        html: str = await self.html_getter.get_html(url, logger)
        raw_total_pages: re.Match[str] | None = re.search(r'"totalPages":(\d+)', html)

        if not raw_total_pages:
            raise PagesCountNotFoundError(url)

        urls: list[str] = []
        total_pages: int = int(raw_total_pages.group(1))

        for page_number in range(1, total_pages + 1):
            parsed_url: ParseResult = urlparse(url)

            unparsed_url: str = urlunparse(
                (
                    parsed_url.scheme,
                    parsed_url.netloc,
                    parsed_url.path,
                    parsed_url.params,
                    f"page={page_number}",
                    parsed_url.fragment,
                ),
            )
            urls.extend(await self._parse(unparsed_url, logger))

        return list(set(urls))

    async def _parse(self, url: str, logger: ILogger | None = None) -> list[str]:
        html: str = await self.html_getter.get_html(url, logger)
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")

        product_tags: ResultSet = soup.find_all("a", attrs={"class": "yi6"})

        return [f"https://www.ozon.ru{tag.attrs["href"]}" for tag in product_tags]
