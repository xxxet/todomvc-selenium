from autologging import logged
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.options import ArgOptions
from urllib3.exceptions import MaxRetryError

CHROME = 'chrome'
CHROMIUM = 'chromium'
FIREFOX = 'firefox'
SAFARI = 'safari'


@logged
class DriverContainer:
    driver_container = None

    def __init__(self, browser, base_url, headless, remote_driver):
        self.driver: WebDriver = None
        self.base_url = base_url
        self.browser_name = browser
        self.headless = headless
        self.remote_driver = remote_driver

    @classmethod
    def create_driver(cls, browser, base_url, headless: bool,
                      remote_driver) -> WebDriver:
        if cls.driver_container is None:
            cls.driver_container = DriverContainer(browser,
                                                   base_url,
                                                   headless,
                                                   remote_driver)
            cls.driver_container.configure_browser()

    @classmethod
    def get_driver_container(cls):
        return cls.driver_container

    @classmethod
    def close_driver(cls):
        if cls.driver_container:
            cls.driver_container.driver.quit()
            cls.driver_container = None

    def configure_browser(self):
        self.__log.info('Configure new browser')
        if self.remote_driver:
            try:
                self._configure_remote_browser()
            except MaxRetryError as retry_error:
                self.__log.error(
                    f"Can't connect to remote driver "
                    f"{self.remote_driver} with browser {self.browser}")
                raise retry_error
        else:
            self._configure_local_browser()

    def _configure_local_browser(self):
        if self.browser_name == CHROME or self.browser_name == CHROMIUM:
            driver = self._configure_local_chrome(self.headless)
        elif self.browser_name == FIREFOX:
            driver = self._configure_local_firefox(self.headless)
        elif self.browser_name == SAFARI:
            driver = self._configure_local_safari(self.headless)
        else:
            raise ValueError(f"Browser {self.browser_name} is not supported")
        self.driver = driver

    def _configure_remote_browser(self):
        if self.browser_name == CHROME:
            driver = self._configure_remote_chrome()
        elif self.browser_name == FIREFOX:
            driver = self._configure_remote_firefox()
        else:
            raise ValueError(f"Browser {self.browser_name} is not supported")
        self.driver = driver

    def _config_for_docker_hub(self, options: ArgOptions):
        pass
        options.set_capability("se:recordVideo", "true")
        options.set_capability("se:screenResolution", "1920x1080")
        # options.add_argument('se:recordVideo=true')
        # options.add_argument('se:screenResolution=1024x768')


    def _configure_remote_firefox(self):
        self.__log.info(f"Starting remote firefox: {self.remote_driver}")
        options = webdriver.FirefoxOptions()
        self._config_for_docker_hub(options)
        if self.headless:
            options.headless = True
            options.add_argument("-width=1920")
            options.add_argument("-height=1080")

        driver = webdriver.Remote(
            command_executor=self.remote_driver,
            options=options
        )

        if not self.headless:
            driver.maximize_window()
        return driver

    def _configure_remote_chrome(self):
        self.__log.info(f"Starting remote chrome: {self.remote_driver}")
        options = webdriver.ChromeOptions()
        self._config_for_docker_hub(options)
        if self.headless:
            options.add_argument('--headless')
            options.add_argument('window-size=1920,1080')
        else:
            options.add_argument('start-maximized')
        driver = webdriver.Remote(
            command_executor=self.remote_driver,
            options=options
        )
        return driver

    def _configure_local_safari(self, headless):
        options = webdriver.SafariOptions()
        if headless:
            options.headless = True
            options.add_argument("-width=1920")
            options.add_argument("-height=1080")
        driver = webdriver.Safari(options=options)
        if not headless:
            driver.maximize_window()
        return driver

    def _configure_local_firefox(self, headless):
        options = webdriver.FirefoxOptions()
        if headless:
            options.headless = True
            options.add_argument("-width=1920")
            options.add_argument("-height=1080")
        driver = webdriver.Firefox(options=options)
        if not headless:
            driver.maximize_window()
        return driver

    def _configure_local_chrome(self, headless):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
            options.add_argument('window-size=1920,1080')
        else:
            options.add_argument('start-maximized')
        driver = webdriver.Chrome(options)
        return driver
