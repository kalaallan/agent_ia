from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Bienvenue sur l'API AI Coach"
    }


def test_cors_headers_present(client, cors_headers):
    response = client.get("/", headers=cors_headers)

    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


def test_app_starts():
    routes = [route.path for route in app.routes]

    assert "/" in routes