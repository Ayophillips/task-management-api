import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient

def test_task_title_length_limits(client: TestClient, auth_headers: dict):
    # Test minimum length
    response = client.post(
        "/tasks/",
        json={
            "title": "",
            "due_date": (date.today() + timedelta(days=1)).isoformat()
        },
        headers=auth_headers
    )
    assert response.status_code == 422

    # Test maximum length (101 characters)
    response = client.post(
        "/tasks/",
        json={
            "title": "x" * 101,
            "due_date": (date.today() + timedelta(days=1)).isoformat()
        },
        headers=auth_headers
    )
    assert response.status_code == 422

def test_task_date_boundaries(client: TestClient, auth_headers: dict):
    # Test past date
    response = client.post(
        "/tasks/",
        json={
            "title": "Past Task",
            "due_date": (date.today() - timedelta(days=1)).isoformat()
        },
        headers=auth_headers
    )
    assert response.status_code == 422

    # Test far future date (> 1 year)
    response = client.post(
        "/tasks/",
        json={
            "title": "Future Task",
            "due_date": (date.today() + timedelta(days=366)).isoformat()
        },
        headers=auth_headers
    )
    assert response.status_code == 422

def test_invalid_enum_values(client: TestClient, auth_headers: dict):
    # Test invalid priority
    response = client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "due_date": (date.today() + timedelta(days=1)).isoformat(),
            "priority": "INVALID"
        },
        headers=auth_headers
    )
    assert response.status_code == 422

    # Test invalid status
    response = client.post(
        "/tasks/",
        json={
            "title": "Test Task",
            "due_date": (date.today() + timedelta(days=1)).isoformat(),
            "status": "INVALID"
        },
        headers=auth_headers
    )
    assert response.status_code == 422