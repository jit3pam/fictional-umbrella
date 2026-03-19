from __future__ import annotations

import logging
from typing import Any

from selenium.webdriver.remote.webdriver import WebDriver

from core.action_executor import ActionExecutor
from core.elements.button import Button
from core.elements.dropdown import Dropdown
from core.elements.input import Input
from core.locator import Locator


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10) -> None:
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout
        self.executor = ActionExecutor(logger=logging.getLogger(self.__class__.__name__))

    def button(self, locator: Locator) -> Button:
        return Button(self.driver, locator, self.timeout)

    def input(self, locator: Locator) -> Input:
        return Input(self.driver, locator, self.timeout)

    def dropdown(self, locator: Locator) -> Dropdown:
        return Dropdown(self.driver, locator, self.timeout)

    def do(self, element: Any, action: str, *args: Any) -> Any:
        return self.executor.execute(element, action, *args)
