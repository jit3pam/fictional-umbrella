from selenium.webdriver.support.ui import Select

from core.base_element import BaseElement


class Dropdown(BaseElement):
    def select_by_text(self, text: str) -> None:
        Select(self.find()).select_by_visible_text(text)
