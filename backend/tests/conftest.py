# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from app.main import app


# ----------------------------
# FASTAPI CLIENT
# ----------------------------
@pytest.fixture(scope="session")
def client():
    return TestClient(app)


# ----------------------------
# PDF FAKE RÉUTILISABLE
# ----------------------------
@pytest.fixture
def fake_pdf_bytes():
    return b"%PDF-1.4 fake pdf content"


# ----------------------------
# DOCUMENT SIMPLE POUR LLM TESTS
# ----------------------------
@pytest.fixture
def simple_document():
    return "Calcule la dérivée de x^2."


# ----------------------------
# HEADERS CORS (réutilisable)
# ----------------------------
@pytest.fixture
def cors_headers():
    return {
        "Origin": "http://localhost:5173"
    }