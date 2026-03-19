from __future__ import annotations

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.locator import Locator


class BaseElement:
    def __init__(self, driver: WebDriver, locator: Locator, timeout: int = 10) -> None:
        self.driver = driver
        self.locator = locator
        self.timeout = timeout

    @property
    def name(self) -> str:
        return self.locator.name or self.__class__.__name__

    def _wait(self) -> WebDriverWait:
        return WebDriverWait(self.driver, self.timeout)

    def find(self) -> WebElement:
        return self._wait().until(EC.visibility_of_element_located(self.locator.unpack()))

    def find_clickable(self) -> WebElement:
        return self._wait().until(EC.element_to_be_clickable(self.locator.unpack()))
