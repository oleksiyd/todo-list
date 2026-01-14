import json
import os
from typing import List
from pathlib import Path
from ..models.todo import Todo
from ..models.list_options import ListOptions
from app.constants import CHARACTER_ENCODING

class TodoService:
    def __init__(self, data_file: str):
        self.data_file_path = Path(data_file)

    # -------------------------
    # Persistence helpers
    # -------------------------
    def _load(self) -> List[Todo]:
        if not self.data_file_path.exists():
            return []
        with self.data_file_path.open("r", encoding=CHARACTER_ENCODING) as f:
            data = json.load(f)
        return [Todo(**item) for item in data]

    def _save(self, todos: List[Todo]) -> None:
        # Ensure parent directory exists
        if not self.data_file_path.parent.is_dir():
            self.data_file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.data_file_path.open("w", encoding=CHARACTER_ENCODING) as f:
            json.dump([t.to_dict() for t in todos], f, indent=2)

    # -------------------------
    # List / filter / sort
    # -------------------------
    def list(self) -> List[Todo]:
        return self.list_filtered()

    def list_filtered(
        self,
        list_options: ListOptions
    ) -> List[Todo]:
        todos = self._load()

        # ---- filter ----
        status = list_options.status
        if status == "completed":
            todos = [t for t in todos if t.isCompleted]
        elif status in ("pending", "incomplete"):
            todos = [t for t in todos if not t.isCompleted]

        # ---- sort ----
        sort_key = list_options.sort
        reverse = list_options.order == "desc"

        if sort_key == "title":
            todos.sort(key=lambda t: (t.title or "").lower(), reverse=reverse)

        elif sort_key == "duedate":
            # Items without dueDate always go last
            todos.sort(
                key=lambda t: (t.dueDate is None, t.dueDate or ""),
                reverse=reverse,
            )

        else:  # createdAt
            todos.sort(key=lambda t: t.createdAt or "", reverse=reverse)

        return todos

    # -------------------------
    # CRUD
    # -------------------------
    def get(self, todo_id: int) -> Todo:
        for todo in self._load():
            if todo.id == todo_id:
                return todo
        raise KeyError(f"Todo {todo_id} not found")

    def add(
        self,
        todo: Todo
    ) -> Todo:
        todos = self._load()
        next_id = max((t.id for t in todos), default=0) + 1

        todo.id=next_id

        todos.append(todo)
        self._save(todos)
        return todo

    def update(
        self,
        updated_todo: Todo
    ) -> Todo:
        todos = self._load()
        for todo in todos:
            if todo.id == updated_todo.id:
                todo.title = updated_todo.title
                todo.description = updated_todo.description
                todo.dueDate = updated_todo.dueDate
                self._save(todos)
                return todo

        raise KeyError(f"Todo {updated_todo.id} not found")

    def set_completed(self, todo_id: int, completed: bool) -> Todo:
        todos = self._load()
        for todo in todos:
            if todo.id == todo_id:
                todo.isCompleted = bool(completed)
                self._save(todos)
                return todo

        raise KeyError(f"Todo {todo_id} not found")

    def delete(self, todo_id: int) -> None:
        todos = self._load()
        remaining = [t for t in todos if t.id != todo_id]

        if len(remaining) == len(todos):
            raise KeyError(f"Todo {todo_id} not found")

        self._save(remaining)
