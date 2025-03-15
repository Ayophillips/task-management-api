import time
import pytest
from statistics import mean
from fastapi.testclient import TestClient
from datetime import date, timedelta

def test_task_list_performance(client: TestClient, auth_headers: dict):
    # Create 100 tasks
    for i in range(100):
        client.post(
            "/tasks/",
            json={
                "title": f"Performance Test Task {i}",
                "due_date": (date.today() + timedelta(days=1)).isoformat()
            },
            headers=auth_headers
        )
    
    # Measure response times for different page sizes
    response_times = []
    for _ in range(10):
        start_time = time.time()
        response = client.get("/tasks/", headers=auth_headers)
        end_time = time.time()
        response_times.append(end_time - start_time)
    
    avg_response_time = mean(response_times)
    assert avg_response_time < 0.5  # Response should be under 500ms

def test_search_performance(client: TestClient, auth_headers: dict):
    # Test search performance with different query lengths
    search_terms = ["Task", "Performance", "Test Task", "NonexistentTask"]
    for term in search_terms:
        start_time = time.time()
        response = client.get(f"/tasks/?title={term}", headers=auth_headers)
        end_time = time.time()
        
        assert end_time - start_time < 0.5  # Search should be under 500ms