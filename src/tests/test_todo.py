import pytest
from assertpy import assert_that

from src.sel.pages.todo_mvc_page import TodoMvcPage


@pytest.mark.usefixtures("get_browser")
class TestTodoMvc:

    @pytest.fixture
    def todos_fixture(self):
        todos = ["My todo1", "My todo2", "My todo3"]
        yield todos
        TodoMvcPage().toggle_todos().clear_completed()

    def test_add_todo(self, todos_fixture):
        todo_page = TodoMvcPage()
        todo_page.open()
        for todo in todos_fixture:
            todo_page.type_todo(todo)
        todo_page.mark_todo_done({todos_fixture[0]: False})
        todos = todo_page.get_created_todos()
        assert_that(todos).is_equal_to([{todos_fixture[0]: True}] + [{todo: False} for todo in todos_fixture[1:]])
