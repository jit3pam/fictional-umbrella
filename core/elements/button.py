from core.base_element import BaseElement


class Button(BaseElement):
    def click(self) -> None:
        self.find_clickable().click()
