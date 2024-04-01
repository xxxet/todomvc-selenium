from typing import List

from selenium.common.exceptions import ElementClickInterceptedException, \
    StaleElementReferenceException, \
    NoSuchElementException, \
    ElementNotVisibleException, \
    ElementNotInteractableException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.driver_container import DriverContainer


class BaseElement:
    timeout = 30
    driver: WebDriver

    def __init__(self,  selector):
        self.selector = selector
        self.driver = DriverContainer.get_driver_container().driver

    def wait_until_ready(self) -> WebElement:
        element = WebDriverWait(self.driver, self.timeout,
                                ignored_exceptions=(ElementClickInterceptedException,
                                                    ElementNotVisibleException,
                                                    NoSuchElementException,
                                                    ElementNotInteractableException,
                                                    StaleElementReferenceException)) \
            .until(EC.element_to_be_clickable(self.selector))
        return element

    def wait_until_visible(self) -> WebElement:
        element = WebDriverWait(self.driver, self.timeout) \
            .until(EC.visibility_of_element_located(self.selector))
        return element

    def wait_until_stale(self, elem) -> bool:
        status = WebDriverWait(self.driver, self.timeout).until(
            EC.staleness_of(elem))
        return status

    def wait_until_present(self) -> WebElement:
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(self.selector))
        return element

    def wait_until_child_clickable(self, select_by) -> WebElement:
        el = self.wait_until_ready()
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(el.find_element(select_by)))
        return element

    def wait_until_not_visible(self) -> WebElement:
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.invisibility_of_element(self.selector))
        return element

    def get_list(self) -> List[WebElement]:
        elements = self.driver.find_elements(*self.selector)
        return elements

    def type(self, text: str):
        self.wait_until_ready().send_keys(text)
        return self

    def type_return(self):
        self.wait_until_ready().send_keys(Keys.RETURN)
        return self

    def click(self):
        self.wait_until_ready().click()
        return self

    def scroll_to(self):
        ActionChains(self.driver). \
            move_to_element(self.wait_until_ready()) \
            .perform()
        return self

    def get_value(self) -> str:
        return self.wait_until_ready().text
