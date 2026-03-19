from __future__ import annotations

import logging
from pathlib import Path
from typing import Any


class ActionExecutor:
    def __init__(self, retries: int = 2, logger: logging.Logger | None = None) -> None:
        self.retries = retries
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    def execute(self, element: Any, action: str, *args: Any) -> Any:
        last_error: Exception | None = None

        for attempt in range(1, self.retries + 2):
            try:
                method = getattr(element, action)
                result = method(*args)
                self._log(element, action, "PASS", attempt=attempt)
                return result
            except Exception as error:  # noqa: BLE001 - executor should centralize failures
                last_error = error
                self._log(element, action, "FAIL", error=error, attempt=attempt)
                self._capture_screenshot(element, action, attempt)
                if attempt > self.retries:
                    raise

        raise last_error  # pragma: no cover

    def _log(
        self,
        element: Any,
        action: str,
        status: str,
        error: Exception | None = None,
        attempt: int = 1,
    ) -> None:
        payload = {
            "element_name": getattr(element, "name", element.__class__.__name__),
            "element_type": element.__class__.__name__,
            "action": action,
            "status": status,
            "attempt": attempt,
            "error_message": str(error) if error else "",
        }
        log_method = self.logger.info if status == "PASS" else self.logger.error
        log_method(payload)

    def _capture_screenshot(self, element: Any, action: str, attempt: int) -> None:
        driver = getattr(element, "driver", None)
        if driver is None or not hasattr(driver, "save_screenshot"):
            return

        screenshots_dir = Path("artifacts/screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{element.__class__.__name__.lower()}_{action}_attempt_{attempt}.png"
        driver.save_screenshot(str(screenshots_dir / filename))
