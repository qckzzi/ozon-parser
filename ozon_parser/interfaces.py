from typing import Any, Protocol

from pydantic import AnyHttpUrl


class ILogger(Protocol):
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None: ...


class IService(Protocol):
    async def __call__(self, url: AnyHttpUrl, logger: ILogger | None = None) -> None: ...
