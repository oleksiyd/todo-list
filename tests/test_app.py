import json
import pytest
from app import create_app
from freezegun import freeze_time
from app.forms.todo_form import TodoForm
from app.constants import CHARACTER_ENCODING

@pytest.fixture
def data_file(tmp_path):
    return tmp_path / "data/todos.json"

@pytest.fixture
def app(data_file):
    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test",
        "DATA_FILE": str(data_file),
    })
    return app

@pytest.fixture
def client(app):
    with app.test_client() as c:
        yield c

def _read_json(path):
    with open(path, "r", encoding=CHARACTER_ENCODING) as f:
        return json.load(f)

def test_add_and_list(client, data_file):
    r = client.post(
        "/add",
        data={"title": "Test Task", "description": "Test description", "dueDate": "2026-01-31"},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"Test Task" in r.data

    todos = _read_json(data_file)
    assert len(todos) == 1
    assert todos[0]["title"] == "Test Task"
    assert todos[0]["description"] == "Test description"
    assert todos[0]["dueDate"] == "2026-01-31"
    assert todos[0]["isCompleted"] is False
    assert todos[0]["createdAt"]

def test_add_and_list_description_duedate_empty(client, data_file):
    r = client.post(
        "/add",
        data={"title": "Test Task"},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert b"Test Task" in r.data

    todos = _read_json(data_file)
    assert len(todos) == 1
    assert todos[0]["title"] == "Test Task"
    assert todos[0]["description"] == None
    assert todos[0]["dueDate"] == None
    assert todos[0]["isCompleted"] is False
    assert todos[0]["createdAt"]

def test_validation_error_shows_form_errors(client):
    r = client.post("/add", data={"title": ""}, follow_redirects=True)
    assert r.status_code == 200
    assert b"Title is required" in r.data

def test_view_update(client, data_file):
    client.post("/add", data={"title": "Todo 1", "description": "", "dueDate": ""})

    r = client.get("/view/1")
    assert r.status_code == 200
    assert b"Todo 1" in r.data

    r2 = client.post(
        "/update/1",
        data={"title": "Todo 2", "description": "Todo 2 description", "dueDate": "2026-02-01"},
        follow_redirects=True,
    )
    assert r2.status_code == 200
    assert b"Todo 2" in r2.data

    todos = _read_json(data_file)
    assert todos[0]["title"] == "Todo 2"
    assert todos[0]["description"] == "Todo 2 description"
    assert todos[0]["dueDate"] == "2026-02-01"

def test_complete_incomplete(client, data_file):
    client.post("/add", data={"title": "Todo"})
    client.get("/complete/1", follow_redirects=True)
    todos = _read_json(data_file)
    assert todos[0]["isCompleted"] is True

    client.get("/incomplete/1", follow_redirects=True)
    todos = _read_json(data_file)
    assert todos[0]["isCompleted"] is False

def test_delete(client, data_file):
    client.post("/add", data={"title": "Delete Me"})
    client.get("/delete/1", follow_redirects=True)

    todos = _read_json(data_file)
    assert todos == []

def test_filter_completed_pending(client):
    client.post("/add", data={"title": "Todo 1"})
    client.post("/add", data={"title": "Todo 2"})
    client.get("/complete/1", follow_redirects=True)

    r_completed = client.get("/?status=completed")
    assert r_completed.status_code == 200
    assert b"Todo 1" in r_completed.data
    assert b"Todo 2" not in r_completed.data

    r_pending = client.get("/?status=pending")
    assert r_pending.status_code == 200
    assert b"Todo 2" in r_pending.data
    assert b"Todo 1" not in r_pending.data

def test_sort_by_title_asc(client):
    client.post("/add", data={"title": "b-task"})
    client.post("/add", data={"title": "a-task"})
    r = client.get("/?sort=title&order=asc")
    assert r.status_code == 200
    html = r.data.decode(CHARACTER_ENCODING)
    assert html.find("a-task") < html.find("b-task")

def test_sort_by_title_desc(client):
    client.post("/add", data={"title": "b-task"})
    client.post("/add", data={"title": "a-task"})
    r = client.get("/?sort=title&order=desc")
    assert r.status_code == 200
    html = r.data.decode(CHARACTER_ENCODING)
    assert html.find("b-task") < html.find("a-task")

def test_sort_by_duedate_asc(client):
    client.post("/add", data={"title": "a-task", "dueDate": "2026-02-01"})
    client.post("/add", data={"title": "b-task", "dueDate": "2026-03-01"})
    r = client.get("/?sort=dueDate&order=asc")
    assert r.status_code == 200
    html = r.data.decode(CHARACTER_ENCODING)
    assert html.find("a-task") < html.find("b-task")

def test_sort_by_duedate_desc(client):
    client.post("/add", data={"title": "a-task", "dueDate": "2026-02-01"})
    client.post("/add", data={"title": "b-task", "dueDate": "2026-03-01"})
    r = client.get("/?sort=dueDate&order=desc")
    assert r.status_code == 200
    html = r.data.decode(CHARACTER_ENCODING)
    assert html.find("b-task") < html.find("a-task")

def test_sort_by_createdat_asc(client):
    with freeze_time("2026-01-01 10:00:00"):
        client.post("/add", data={"title": "a-task"})
    with freeze_time("2026-01-01 10:00:01"):
        client.post("/add", data={"title": "b-task"})
    r = client.get("/?sort=createdAt&order=asc")
    assert r.status_code == 200
    html = r.data.decode(CHARACTER_ENCODING)
    assert html.find("a-task") < html.find("b-task")

def test_sort_by_createdat_desc(client):
    with freeze_time("2026-01-01 10:00:00"):
        client.post("/add", data={"title": "a-task"})
    with freeze_time("2026-01-01 10:00:01"):
        client.post("/add", data={"title": "b-task"})
    r = client.get("/?sort=createdAt&order=desc")
    assert r.status_code == 200
    html = r.data.decode(CHARACTER_ENCODING)
    assert html.find("b-task") < html.find("a-task")

def test_to_model_requires_validation(app):
    with app.app_context():
        form = TodoForm(data={"title": "Test 1"})
        with pytest.raises(RuntimeError):
            form.to_model()

def test_to_model_after_validation_ok(app):
    with app.app_context():
        form = TodoForm(data={"title": "Test 1"})
        assert form.validate() is True
        todo = form.to_model(todo_id=1)
        assert todo.title == "Test 1"
