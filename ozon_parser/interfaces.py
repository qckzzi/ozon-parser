from typing import Protocol

from pydantic import AnyHttpUrl


class ILogger(Protocol):
    def debug(self, msg: str) -> None: ...


class IService(Protocol):
    async def __call__(self, url: AnyHttpUrl, logger: ILogger | None = None) -> None: ...
