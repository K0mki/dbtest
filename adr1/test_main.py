from main import *
from fastapi.testclient import TestClient

app = FastAPI()
client = TestClient(app)

def test_index():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello'}