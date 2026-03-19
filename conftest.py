import logging
from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchDriverException, WebDriverException
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session", autouse=True)
def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")


@pytest.fixture
def driver() -> Generator[webdriver.Chrome, None, None]:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.set_capability("webSocketUrl", True)

    try:
        browser = webdriver.Chrome(options=options)
    except (NoSuchDriverException, WebDriverException) as error:
        pytest.skip(f"Chrome WebDriver is unavailable in this environment: {error}")

    try:
        yield browser
    finally:
        browser.quit()
