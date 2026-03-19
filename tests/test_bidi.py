import base64
import importlib
import pkgutil

import pytest
from selenium.webdriver.common.by import By

trio = pytest.importorskip("trio")


BIDI_REQUIRES = "BiDi support requires a recent Chrome/ChromeDriver and Selenium build."


def _load_devtools_modules():
    base_package = importlib.import_module("selenium.webdriver.common.devtools")
    version_names = sorted(
        module.name
        for module in pkgutil.iter_modules(base_package.__path__)
        if module.name.startswith("v") and module.name[1:].isdigit()
    )
    if not version_names:
        pytest.skip("No Selenium DevTools modules are available in this environment.")

    latest_version = version_names[-1]
    network = importlib.import_module(f"selenium.webdriver.common.devtools.{latest_version}.network")
    performance = importlib.import_module(f"selenium.webdriver.common.devtools.{latest_version}.performance")
    return network, performance


def _run_trio(async_fn, driver) -> None:
    if not hasattr(driver, "bidi_connection"):
        pytest.skip(BIDI_REQUIRES)
    trio.run(async_fn, driver)


def test_basic_auth(driver):
    network, _ = _load_devtools_modules()
    headers_cls = getattr(network, "Headers")

    async def scenario(browser):
        async with browser.bidi_connection() as connection:
            await connection.session.execute(connection.devtools.network.enable())

            credentials = base64.b64encode(b"admin:admin").decode()
            authorization = {"authorization": f"Basic {credentials}"}
            await connection.session.execute(
                connection.devtools.network.set_extra_http_headers(headers_cls(authorization))
            )

            browser.get("https://the-internet.herokuapp.com/basic_auth")

    _run_trio(scenario, driver)

    success = driver.find_element(By.TAG_NAME, "p")
    assert success.text == "Congratulations! You must have the proper credentials."


def test_performance(driver):
    _, performance = _load_devtools_modules()
    driver.get("https://www.selenium.dev/selenium/web/frameset.html")

    async def scenario(browser):
        async with browser.bidi_connection() as connection:
            await connection.session.execute(connection.devtools.performance.enable())
            metric_list = await connection.session.execute(connection.devtools.performance.get_metrics())
            return {metric.name: metric.value for metric in metric_list}

    if not hasattr(driver, "bidi_connection"):
        pytest.skip(BIDI_REQUIRES)

    metrics = trio.run(scenario, driver)

    assert metrics["DevToolsCommandDuration"] > 0
    assert metrics["Frames"] == 12


def test_set_cookie(driver):
    network, _ = _load_devtools_modules()

    async def scenario(browser):
        async with browser.bidi_connection() as connection:
            await connection.session.execute(
                connection.devtools.network.set_cookie(
                    name="cheese",
                    value="gouda",
                    domain="www.selenium.dev",
                    secure=True,
                )
            )

    _run_trio(scenario, driver)

    driver.get("https://www.selenium.dev")
    cheese = driver.get_cookie("cheese")

    assert cheese is not None
    assert cheese["value"] == "gouda"
