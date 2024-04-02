from pydantic import AmqpDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    amqp_dsn: AmqpDsn
    queue_prefix: str = "parsing."

    selenium_timeout: float = 5.0
    selenium_binary_location: str
    selenium_executable_path: str

    ozon_name: str = "ozon"
    parsed_loading_queue_prefix: str = "parsed_loading."

    @property
    def ozon_queue(self) -> str:
        return f"{self.queue_prefix}{self.ozon_name}"

    @property
    def parsed_loading_queue(self) -> str:
        return f"{self.parsed_loading_queue_prefix}{self.ozon_name}"

    @property
    def amqp_dsn_str(self) -> str:
        return self.amqp_dsn.unicode_string()
