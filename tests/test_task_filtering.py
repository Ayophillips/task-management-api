import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient

@pytest.fixture
def sample_tasks(client: TestClient, auth_headers: dict):
    tasks = [
        {
            "title": "High Priority Task",
            "description": "Urgent task",
            "due_date": (date.today() + timedelta(days=1)).isoformat(),
            "priority": "HIGH",
            "status": "PENDING"
        },
        {
            "title": "Medium Task Today",
            "description": "Regular task",
            "due_date": date.today().isoformat(),
            "priority": "MEDIUM",
            "status": "IN_PROGRESS"
        },
        {
            "title": "Low Priority Task",
            "description": "Can wait",
            "due_date": (date.today() + timedelta(days=7)).isoformat(),
            "priority": "LOW",
            "status": "COMPLETED"
        }
    ]
    
    for task in tasks:
        client.post("/tasks/", json=task, headers=auth_headers)

def test_multiple_filters(client: TestClient, auth_headers: dict, sample_tasks):
    response = client.get(
        "/tasks/",
        params={
            "priority": "HIGH",
            "status": "PENDING",
            "due_date": date.today().isoformat()
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for task in data:
        assert task["priority"] == "HIGH"
        assert task["status"] == "PENDING"

def test_text_search(client: TestClient, auth_headers: dict, sample_tasks):
    response = client.get(
        "/tasks/",
        params={"title": "Priority"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all("Priority" in task["title"] for task in data)