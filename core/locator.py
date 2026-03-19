from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Locator:
    locator: Tuple[str, str]
    name: str | None = None

    def unpack(self) -> Tuple[str, str]:
        return self.locator
