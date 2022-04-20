import pytest
from main import app
from httpx import AsyncClient

@pytest.mark.anyio
async def test_index():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {'Message': 'Go to http://127.0.0.1:8000/docs for the API doc'}