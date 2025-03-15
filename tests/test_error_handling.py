import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
from datetime import date, timedelta

def test_concurrent_updates(client: TestClient, auth_headers: dict):
    # Create a task
    response = client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "due_date": (date.today() + timedelta(days=1)).isoformat()
        },
        headers=auth_headers
    )
    task_id = response.json()["id"]
    
    # Simulate concurrent updates
    update_data = {"title": "Updated Title"}
    response1 = client.put(f"/tasks/{task_id}", json=update_data, headers=auth_headers)
    response2 = client.put(f"/tasks/{task_id}", json=update_data, headers=auth_headers)
    
    assert response1.status_code == 200
    assert response2.status_code == 200  # Should handle concurrent updates gracefully

def test_database_connection_error(client: TestClient, auth_headers: dict, monkeypatch):
    def mock_db_error(*args, **kwargs):
        raise SQLAlchemyError("Database connection failed")
    
    monkeypatch.setattr("sqlmodel.Session.exec", mock_db_error)
    
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 500
    assert "database error" in response.json()["detail"].lower()