import allure
from autologging import logged
from selenium.webdriver.common.by import By
from tenacity import retry, stop_after_attempt, wait_fixed

from src.sel.elements.base_element import BaseElement
from src.sel.pages.base_page import BasePage


@logged
class TodoMvcPage(BasePage):
    todo_input = (By.CSS_SELECTOR, "input[data-testid=text-input]")
    todo_item = (By.CSS_SELECTOR, "li[data-testid=todo-item]")
    toggle_todo = (By.CSS_SELECTOR, "[data-testid=todo-item-toggle]")
    delete_todo_btn = (By.CSS_SELECTOR, "[data-testid='todo-item-button']")
    toggle_all_btn = (By.CSS_SELECTOR, "[data-testid='toggle-all']")
    clear_completed_btn = (By.XPATH, "*//button[contains(., 'Clear completed')]")

    def __init__(self):
        super().__init__()
        self.created_todos = []

    @allure.step
    def open(self):
        self.driver_container.driver.get(self.driver_container.base_url)
        self.has_loaded()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    @allure.step
    def has_loaded(self):
        BaseElement(self.todo_input).wait_until_visible()
        return self

    @allure.step
    def type_todo(self, text):
        BaseElement(self.todo_input) \
            .type(text) \
            .type_return()
        return self

    def _get_todo_els(self):
        return BaseElement(self.todo_item).get_list()

    @allure.step
    def get_created_todos(self):
        todo_lines = self._get_todo_els()
        self.created_todos = [{line.text: line.find_element(*self.toggle_todo).is_selected()} for line in todo_lines]
        return self.created_todos

    def get_todo_names(self):
        todos = [list(todo.keys()) for todo in self.created_todos]
        return [name for todo in todos for name in todo]

    @allure.step
    def mark_todo_done(self, todo):
        self.get_created_todos()
        index_of = self.created_todos.index(todo)
        self._get_todo_els()[index_of].find_element(*self.toggle_todo).click()
        return self

    @allure.step
    def delete_todo(self, todo):
        self.get_created_todos()
        index_of = self.get_todo_names().index(todo)
        self._get_todo_els()[index_of].find_element(*self.delete_todo_btn).click()

    @allure.step
    def toggle_todos(self):
        BaseElement(self.toggle_all_btn).wait_until_present().click()
        return self

    @allure.step
    def clear_completed(self):
        BaseElement(self.clear_completed_btn).wait_until_present().click()
        return self
