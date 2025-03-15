from fastapi.testclient import TestClient
from sqlmodel import Session
import pytest
from datetime import datetime

def test_register_user(client: TestClient):
    response = client.post(
        "/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "Password123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "id" in data
    assert "is_active" in data
    assert "created_at" in data

def test_register_duplicate_email(client: TestClient, test_user):
    response = client.post(
        "/register",
        json={
            "email": test_user["email"],
            "username": "different_user",
            "password": "Password123!"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_success(client: TestClient, test_user):
    response = client.post(
        "/token",
        data={
            "username": test_user["username"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/token",
        data={
            "username": "wronguser",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401