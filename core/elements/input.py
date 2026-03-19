from core.base_element import BaseElement


class Input(BaseElement):
    def type(self, text: str) -> None:
        element = self.find()
        element.clear()
        element.send_keys(text)
