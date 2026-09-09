import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.app import create_app


def make_app():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    app = create_app(test_config={"TESTING": True, "DB_PATH": path})
    return app, path


def test_health():
    app, _ = make_app()
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_add_and_list_todo():
    app, _ = make_app()
    client = app.test_client()
    resp = client.post("/api/todos", json={"title": "belajar devops"})
    assert resp.status_code == 201
    assert resp.get_json()["title"] == "belajar devops"

    resp = client.get("/api/todos")
    assert resp.status_code == 200
    todos = resp.get_json()
    assert len(todos) == 1


def test_add_todo_requires_title():
    app, _ = make_app()
    client = app.test_client()
    resp = client.post("/api/todos", json={})
    assert resp.status_code == 400


def test_toggle_todo():
    app, _ = make_app()
    client = app.test_client()
    todo = client.post("/api/todos", json={"title": "test"}).get_json()
    resp = client.patch(f"/api/todos/{todo['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["done"] == 1
