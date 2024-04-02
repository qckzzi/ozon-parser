from collections.abc import Mapping, Sequence

from bakery import Bakery, Cake
from faststream.rabbit import RabbitBroker, RabbitQueue, RabbitRoute, RabbitRouter
from selenium_async.pool import Pool

from ozon_parser.adapters.selenium import SeleniumClient
from ozon_parser.config import Settings
from ozon_parser.handler import ParsingHandler
from ozon_parser.interfaces import IService
from ozon_parser.models import EntityType
from ozon_parser.parsers.product.parser import ProductParser
from ozon_parser.parsers.product_characteristic.parser import ProductCharacteristicsParser
from ozon_parser.parsers.product_image.parser import ProductImagesParser
from ozon_parser.parsers.product_main_data.parser import ProductMainDataParser
from ozon_parser.publishers.mq import ParsedProductMQPublisher
from ozon_parser.services.product.service import ProductService


class Container(Bakery):
    settings: Settings = Cake(Settings)  # type: ignore[assignment]

    broker: RabbitBroker = Cake(RabbitBroker, settings.amqp_dsn_str)
    _parsed_product_mq_publisher: ParsedProductMQPublisher = Cake(
        ParsedProductMQPublisher,
        broker,
        settings.parsed_loading_queue,
    )

    _pool: Pool = Cake(Pool, blank_page_after_use=False)
    _selenium_client: SeleniumClient = Cake(
        SeleniumClient,
        pool=_pool,
        timeout=settings.selenium_timeout,
        executable_path=settings.selenium_executable_path,
        binary_location=settings.selenium_binary_location,
    )

    _product_main_data_parser: ProductMainDataParser = Cake(ProductMainDataParser)
    _product_images_parser: ProductImagesParser = Cake(ProductImagesParser)
    _product_characteristics_parser: ProductCharacteristicsParser = Cake(ProductCharacteristicsParser)
    _product_parser: ProductParser = Cake(
        ProductParser,
        main_data_parser=_product_main_data_parser,
        images_parser=_product_images_parser,
        characteristics_parser=_product_characteristics_parser,
    )

    _product_service: ProductService = Cake(
        ProductService,
        product_parser=_product_parser,
        html_getter=_selenium_client,
        publisher=_parsed_product_mq_publisher,
    )
    _services_by_entity_types: Mapping[EntityType, IService | None] = Cake(
        {
            "PRODUCT": _product_service,
            "CATEGORY": None,
            "SELLER": None,
            "BRAND": None,
        },
    )

    _parsing_handler: ParsingHandler = Cake(ParsingHandler, _services_by_entity_types)
    _ozon_queue: RabbitQueue = Cake(RabbitQueue, settings.ozon_queue, durable=True)
    _ozon_route: RabbitRoute = Cake(RabbitRoute, _parsing_handler, _ozon_queue)

    _routes: Sequence[RabbitRoute] = (_ozon_route,)
    router: RabbitRouter = Cake(RabbitRouter, handlers=_routes)

    queues_to_declare: list[str] = Cake([settings.parsed_loading_queue])
