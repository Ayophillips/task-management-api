import asyncio
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from datetime import date, timedelta

@pytest.mark.asyncio
async def test_concurrent_task_creation(auth_headers: dict):
    async with AsyncClient(base_url="http://test") as ac:
        tasks = []
        for i in range(10):
            task = ac.post(
                "/tasks/",
                json={
                    "title": f"Concurrent Task {i}",
                    "due_date": (date.today() + timedelta(days=1)).isoformat()
                },
                headers=auth_headers
            )
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        assert all(r.status_code == 201 for r in responses)