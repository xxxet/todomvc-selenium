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
        todos = [["My todo1", False], ["My todo2", False], ["My todo3", False]]
        yield todos
        TodoMvcPage().toggle_todos().clear_completed()

    def test_add_todo_fail(self, todos_fixture):
        todo_page = TodoMvcPage()
        todo_page.open()
        for todo in todos_fixture:
            todo_page.create_todo(*todo)
        todo_page.mark_todo_done(*todos_fixture[0])
        todos = todo_page.get_created_todos()
        assert_that(todos).is_equal_to(todos_fixture)

    def test_add_todo(self, todos_fixture):
        todo_page = TodoMvcPage()
        todo_page.open()
        for todo in todos_fixture:
            todo_page.create_todo(*todo)
        todo_page.mark_todo_done(*todos_fixture[0])
        todos = todo_page.get_created_todos()
        assert_that(todos).is_equal_to([[todos_fixture[0][0], True]] + todos_fixture[1:])


