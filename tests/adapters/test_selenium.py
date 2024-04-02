from typing import Any

from faker import Faker
from pytest_mock import MockFixture

from ozon_parser.adapters.selenium import SeleniumClient


def test_get_html(html: str, mocker: MockFixture, faker: Faker) -> None:
    driver: Any = mocker.Mock(page_source=html)
    selenium: SeleniumClient = SeleniumClient(driver)
    url: str = faker.url()
    assert html == selenium.get_html(url=url)
    assert driver.get.mock_calls == [
        mocker.call(url),
    ]
