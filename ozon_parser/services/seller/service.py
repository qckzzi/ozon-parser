import typing
from collections.abc import Sequence

from pydantic import AnyHttpUrl
from pydantic_core import Url

from ozon_parser.interfaces import ILogger
from ozon_parser.services.seller.interfaces import IProductService, ISellerParser


class SellerService:
    def __init__(
        self,
        product_service: IProductService,
        seller_parser: ISellerParser,
    ) -> None:
        self.product_service: typing.Final[IProductService] = product_service
        self.seller_parser: typing.Final[ISellerParser] = seller_parser

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]"

    async def __call__(self, url: AnyHttpUrl, logger: ILogger | None = None) -> None:
        if logger:
            logger.debug(f"{self} processes {url=}")

        product_urls: Sequence[str] = await self.seller_parser.parse(url.unicode_string(), logger)

        for p_url in product_urls:
            try:
                await self.product_service(Url(p_url), logger)
            except Exception:  # noqa: BLE001
                if logger:
                    logger.exception("Found an error while product processing")
