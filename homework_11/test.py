from fastapi.testclient import TestClient

from main import app

from socket import gethostname


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    data = response.json()
    assert response.status_code == 200
    assert data["hostname"] == gethostname()


def test_health_check():
    response = client.get("/isalive")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
