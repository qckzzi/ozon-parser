from typing import Protocol

from ozon_parser.interfaces import ILogger


class IHtmlGetter(Protocol):
    async def get_html(self, url: str, logger: ILogger | None = None) -> str: ...
