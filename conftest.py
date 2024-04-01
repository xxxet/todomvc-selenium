import logging

import allure
import pytest

from src.utils.driver_container import DriverContainer

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-4s %(levelname)-4s %(message)s', datefmt='%H:%M:%S')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def pytest_addoption(parser):
    parser.addoption("--url",
                     action="store",
                     default="https://todomvc.com/examples/react/dist/",
                     help="Base url to be used in tests")
    parser.addoption('--headless',
                     default=False,
                     action="store_true",
                     help='Run browser in headless mode')
    parser.addoption("--browser",
                     action="store",
                     default="chrome",
                     help="Name of the browser")
    parser.addoption("--remote_driver",
                     action="store",
                     default=None,
                     help="Url of the remote driver")


@pytest.fixture
def get_browser(request):
    logger.info(f"Setup for {request.node.name}")
    base_url = request.config.getoption("--url")
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    remote_driver = request.config.getoption("--remote_driver")
    DriverContainer.create_driver(browser, base_url, headless, remote_driver)
    yield
    logger.info("Closing driver")
    DriverContainer.close_driver()


def pytest_exception_interact(node, call, report):
    driver = DriverContainer.get_driver_container().driver
    if driver is not None:
        allure.attach(driver.get_screenshot_as_png(),
                      "screenshot",
                      allure.attachment_type.PNG)
