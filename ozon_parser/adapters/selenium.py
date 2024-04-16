from selenium.webdriver import Firefox, FirefoxOptions, FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium_async.pool import Pool  # type: ignore[import-untyped]

from ozon_parser.interfaces import ILogger


class SeleniumClient:
    def __init__(self, *, pool: Pool, executable_path: str, binary_location: str, timeout: float = 10.0) -> None:
        self.pool: Pool = pool
        self.timeout: float = timeout
        self.executable_path: str = executable_path
        self.binary_location: str = binary_location

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]"

    async def get_html(self, url: str, logger: ILogger | None = None) -> str:
        if logger:
            logger.debug(f"{self} fetches html from {url=}")

        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")

        firefox_options.binary_location = self.binary_location

        driver: Firefox = Firefox(
            options=firefox_options,
            service=FirefoxService(executable_path=self.executable_path),
        )

        driver.get(url)
        driver.get(url)
        WebDriverWait(driver, self.timeout).until(
            ec.presence_of_element_located((By.XPATH, '//div[@id="section-characteristics"]')),
        )
        WebDriverWait(driver, self.timeout).until(
            ec.presence_of_element_located((By.XPATH, '//div[@id="section-description"]')),
        )

        return driver.page_source
