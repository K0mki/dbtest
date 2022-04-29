import pytest
from httpx import AsyncClient
from main import *

ac = AsyncClient(app=app, base_url="http://test")


contact = {
    "id": "1x",
    "first_name": "Test",
    "last_name": "Test1"
}


@pytest.mark.anyio
async def test_index():
    response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {
        'Message': 'Go to http://127.0.0.1:8000/docs for the API doc'}


# @pytest.mark.anyio
# async def test_init():
#     response = await ac.post("/init")
#     assert response.status_code == 200  # TODO ??
#     assert response.json() == {"Database created"}


@pytest.mark.anyio
async def test_add_phone_type():
    response = await ac.post("/api/contacts/types/add", json={
        "name": "Test"
    })
    assert response.status_code == 200  # TODO ??
    assert response.json() == {"Created phone type": {"Test"}}


# @pytest.mark.anyio
# async def test_delete_contact():
#     response = await ac.delete("/contacts/{contact_id}")
#     assert response.status_code == 200
#     assert response.json() == {"Phone deleted": "{contact_id}"}
