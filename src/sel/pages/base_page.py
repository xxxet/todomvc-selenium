from src.utils.driver_container import DriverContainer


class BasePage:
    def __init__(self):
        self.driver_container: DriverContainer = DriverContainer.get_driver_container()
