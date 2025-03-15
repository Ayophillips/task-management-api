from fastapi.testclient import TestClient
from sqlmodel import Session
import pytest
from datetime import date, timedelta

def get_auth_headers(client: TestClient, test_user: dict) -> dict:
    response = client.post(
        "/token",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def auth_headers(client: TestClient, test_user: dict) -> dict:
    return get_auth_headers(client, test_user)

def test_create_task(client: TestClient, auth_headers: dict):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": (date.today() + timedelta(days=1)).isoformat(),
        "priority": "MEDIUM",
        "status": "PENDING"
    }
    
    response = client.post(
        "/tasks/",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert "id" in data
    assert "user_id" in data

def test_create_task_invalid_date(client: TestClient, auth_headers: dict):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": (date.today() - timedelta(days=1)).isoformat(),
        "priority": "MEDIUM",
        "status": "PENDING"
    }
    
    response = client.post(
        "/tasks/",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 422
    assert "Due date cannot be in the past" in str(response.json())

def test_get_tasks(client: TestClient, auth_headers: dict):
    # First create a task
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": (date.today() + timedelta(days=1)).isoformat(),
        "priority": "MEDIUM",
        "status": "PENDING"
    }
    client.post("/tasks/", json=task_data, headers=auth_headers)
    
    # Now get all tasks
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["title"] == task_data["title"]

def test_update_task(client: TestClient, auth_headers: dict):
    # First create a task
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": (date.today() + timedelta(days=1)).isoformat(),
        "priority": "MEDIUM",
        "status": "PENDING"
    }
    create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    # Update the task
    update_data = {
        "title": "Updated Task",
        "status": "COMPLETED"
    }
    response = client.put(
        f"/tasks/{task_id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["status"] == update_data["status"]
    assert data["description"] == task_data["description"]

def test_delete_task(client: TestClient, auth_headers: dict):
    # First create a task
    task_data = {
        "title": "Test Task",
        "due_date": (date.today() + timedelta(days=1)).isoformat(),
    }
    create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = create_response.json()["id"]
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify task is deleted
    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404