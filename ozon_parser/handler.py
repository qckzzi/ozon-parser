from collections.abc import Mapping
from typing import Annotated, Final

from faststream import Header, Logger
from pydantic import AnyHttpUrl

from ozon_parser.interfaces import IService
from ozon_parser.models import EntityType


_HeaderEntityType = Annotated[EntityType, Header("ENTITY_TYPE")]


class ParsingHandler:
    def __init__(
        self,
        services_by_entity_types: Mapping[EntityType, IService | None],
    ) -> None:
        self.services_by_entity_types: Final[Mapping] = services_by_entity_types

    async def __call__(
        self,
        url: AnyHttpUrl,
        entity_type: _HeaderEntityType,
        logger: Logger,
    ) -> None:
        logger.debug(f"{url=}, {entity_type=}")
        service: IService | None = self.services_by_entity_types[entity_type]

        if service is None:
            logger.warning(f"Service for {entity_type=} is not implemented.")
            return

        await service(url, logger)
