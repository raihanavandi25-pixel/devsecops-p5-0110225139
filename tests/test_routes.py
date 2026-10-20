import pytest

from app import create_app, models
from app.config import TestConfig


@pytest.fixture()
def client():
    models.reset_memory_db()
    app = create_app(TestConfig)
    yield app.test_client()
    models.reset_memory_db()


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_create_and_list(client):
    r = client.post("/tasks", json={"title": "Tugas P5"})
    assert r.status_code == 201
    tasks = client.get("/tasks").get_json()
    assert len(tasks) == 1 and tasks[0]["title"] == "Tugas P5"


def test_create_invalid(client):
    assert client.post("/tasks", json={"title": ""}).status_code == 400


def test_update_and_filter(client):
    tid = client.post("/tasks", json={"title": "A"}).get_json()["id"]
    assert client.patch(f"/tasks/{tid}", json={"status": "done"}).status_code == 200
    assert len(client.get("/tasks?status=done").get_json()) == 1
    assert client.get("/tasks?status=xxx").status_code == 400


def test_update_not_found_and_invalid(client):
    assert client.patch("/tasks/99", json={"status": "done"}).status_code == 404
    assert client.patch("/tasks/1", json={"status": "?"}).status_code == 400


def test_sql_injection_attempt_is_harmless(client):
    client.post("/tasks", json={"title": "x'); DROP TABLE tasks;--"})
    assert len(client.get("/tasks").get_json()) == 1


def test_delete(client):
    tid = client.post("/tasks", json={"title": "A"}).get_json()["id"]
    assert client.delete(f"/tasks/{tid}").status_code == 204
    assert client.delete(f"/tasks/{tid}").status_code == 404
