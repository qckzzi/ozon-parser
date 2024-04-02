from pydantic import AnyHttpUrl

from ozon_parser.interfaces import ILogger
from ozon_parser.services.interfaces import IHtmlGetter, IProduct, IProductParser, IPublisher


class ProductService:
    def __init__(
        self,
        product_parser: IProductParser,
        html_getter: IHtmlGetter,
        publisher: IPublisher,
    ) -> None:
        self.parser: IProductParser = product_parser
        self.html_getter: IHtmlGetter = html_getter
        self.publisher: IPublisher = publisher

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]"

    async def __call__(self, url: AnyHttpUrl, logger: ILogger | None = None) -> None:
        if logger:
            logger.debug(f"{self} processes {url=}")

        html: str = await self.html_getter.get_html(url=url.unicode_string(), logger=logger)
        product: IProduct = self.parser.parse(html)

        if logger:
            logger.debug(f"{self} got '{product.name}' product")

        await self.publisher.publish(
            {
                "name": product.name,
                "brand": product.brand,
                "characteristics": [{"name": ch.name, "value": ch.value} for ch in product.characteristics],
                "description": product.description,
                "images": product.images,
                "sku": product.sku,
            },
            logger,
        )
