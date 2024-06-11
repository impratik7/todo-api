import pytest
from fastapi.testclient import TestClient

def test_create_task(client: TestClient, token: str):
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Task test 1", "description": "This is a test 1st task", "completed": False, "id": 100}
    )
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.json()}")
    assert response.status_code == 200, f"Task creation failed: {response.json()}"
    assert response.json()["title"] == "Task test 1"

def test_read_tasks(client: TestClient, token: str):
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_task(client: TestClient, token: str):
    response = client.get(
        "/tasks/100",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Task test 1"

def test_update_task(client: TestClient, token: str):
    response = client.put(
        "/tasks/100",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Updated Task", "description": "This is an updated task", "completed": True, "id": 100}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"

def test_delete_task(client: TestClient, token: str):
    response = client.delete(
        "/tasks/100",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"