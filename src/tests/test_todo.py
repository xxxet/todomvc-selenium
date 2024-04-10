import time

import pytest
from assertpy import assert_that
from autologging import logged

from src.sel.pages.todo_mvc_page import TodoMvcPage


@logged
@pytest.mark.usefixtures("get_browser")
class TestTodoMvc:

    @pytest.fixture
    def todos_fixture(self):
        todos = ["My todo1", "My todo2", "My todo3"]
        yield todos
        TodoMvcPage().toggle_todos().clear_completed()

    def test_add_todo(self, todos_fixture):
        self.__log.info('Open TodoMvcPage')
        todo_page = TodoMvcPage()
        todo_page.open()
        self.__log.info('Type todos')
        for todo in todos_fixture:
            todo_page.type_todo(todo)
            self.__log.info('Mark todo done')
        todo_page.mark_todo_done({todos_fixture[0]: False})
        self.__log.info('Get created todos')
        todos = todo_page.get_created_todos()
        self.__log.info('assert todos')
        assert_that(todos).is_equal_to([{todos_fixture[0]: False}] + [{todo: False} for todo in todos_fixture[1:]])
