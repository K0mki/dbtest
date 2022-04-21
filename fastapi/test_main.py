import pytest
from httpx import AsyncClient
from main import app

ac = AsyncClient(app=app, base_url="http://test")

@pytest.mark.anyio
async def test_index():
    response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {'Message': 'Go to http://127.0.0.1:8000/docs for the API doc'}


# @pytest.mark.anyio
# async def test_init():
#     response = await ac.get("/init")
#     assert response.status_code == 200
#     assert response.json() == {"Database created"}
