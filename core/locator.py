from dataclasses import dataclass
from typing import Tuple

from selenium.webdriver.common.by import By


@dataclass(frozen=True)
class Locator:
    by: str
    value: str
    name: str | None = None

    @property
    def tuple(self) -> Tuple[str, str]:
        return self.by, self.value

    def unpack(self) -> Tuple[str, str]:
        return self.tuple
