import pytest
from faker import Faker


@pytest.fixture(name="html")
def html_fixture(faker: Faker):
    html: str = f"""
    <!-- index.html -->

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>{faker.word()}</title>
    </head>
    <body>
    {faker.sentence()}
    </body>
    </html>
    """

    return html
