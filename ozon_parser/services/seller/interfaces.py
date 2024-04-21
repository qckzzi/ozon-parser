import typing

from pydantic import AnyHttpUrl

from ozon_parser.interfaces import ILogger


class IProductService(typing.Protocol):
    async def __call__(self, url: AnyHttpUrl, logger: ILogger | None = None) -> None: ...


class ISellerParser(typing.Protocol):
    async def parse(self, url: str, logger: ILogger | None = None) -> typing.Sequence[str]: ...
