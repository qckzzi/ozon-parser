import time

import backoff
import undetected_chromedriver as uc  # type: ignore[import-untyped]
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from ozon_parser.interfaces import ILogger


class ProductHtmlGetter:
    def __init__(self, *, timeout: float = 10.0) -> None:
        self.timeout: float = timeout

    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]"

    def get_html(self, url: str, logger: ILogger | None = None) -> str:
        if logger:
            logger.debug(f"{self} fetches html from {url=}")

        @backoff.on_exception(
            backoff.expo,
            (TimeoutException, NoSuchElementException),
            max_tries=3,
            logger=logger,  # type: ignore[arg-type]
        )
        def _get_html(url: str) -> str:
            page_source: str
            try:
                driver: uc.Chrome = uc.Chrome()
                driver.get(url)
                WebDriverWait(driver, self.timeout).until(
                    ec.presence_of_element_located((By.XPATH, '//div[@id="section-characteristics"]')),
                )
                WebDriverWait(driver, self.timeout).until(
                    ec.presence_of_element_located((By.XPATH, '//div[@id="section-description"]')),
                )
                page_source = driver.page_source
            except TimeoutException:
                button: uc.WebElement = driver.find_element(value="reload-button")
                time.sleep(1)
                button.click()
                WebDriverWait(driver, self.timeout).until(
                    ec.presence_of_element_located((By.XPATH, '//div[@id="section-characteristics"]')),
                )
                WebDriverWait(driver, self.timeout).until(
                    ec.presence_of_element_located((By.XPATH, '//div[@id="section-description"]')),
                )
                page_source = driver.page_source
            finally:
                driver.quit()

            return page_source

        return _get_html(url)
