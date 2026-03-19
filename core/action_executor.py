from __future__ import annotations

import logging
from pathlib import Path
from typing import Any


class ActionExecutor:
    def __init__(self, retries: int = 2, logger: logging.Logger | None = None) -> None:
        self.retries = retries
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    def execute(self, element: Any, action: str, *args: Any) -> Any:
        method = getattr(element, action)
        last_error: Exception | None = None

        for attempt in range(1, self.retries + 2):
            try:
                result = method(*args)
                self._log(element, action, "PASS", attempt)
                return result
            except Exception as error:  # noqa: BLE001 - centralize action failures in one place
                last_error = error
                is_final_attempt = attempt == self.retries + 1
                self._log(element, action, "FAIL", attempt, error)
                if is_final_attempt:
                    self._capture_screenshot(element, action)
                    raise

        raise last_error  # pragma: no cover

    def _log(
        self,
        element: Any,
        action: str,
        status: str,
        attempt: int,
        error: Exception | None = None,
    ) -> None:
        payload = {
            "element_name": getattr(element, "name", element.__class__.__name__),
            "element_type": element.__class__.__name__,
            "action": action,
            "status": status,
            "error_message": str(error) if error else "",
            "attempt": attempt,
        }
        log_method = self.logger.info if status == "PASS" else self.logger.error
        log_method(payload)

    def _capture_screenshot(self, element: Any, action: str) -> None:
        driver = getattr(element, "driver", None)
        if driver is None or not hasattr(driver, "save_screenshot"):
            return

        screenshots_dir = Path("artifacts/screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        element_name = getattr(element, "name", element.__class__.__name__).lower().replace(" ", "_")
        screenshot_path = screenshots_dir / f"{element_name}_{action}.png"
        driver.save_screenshot(str(screenshot_path))
