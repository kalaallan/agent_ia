import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app
from ...utils.pdf_factory import create_simple_pdf

client = TestClient(app)


@pytest.mark.integration
@patch("app.api.agents.comprehension.analyser_pdf_with_trace")
def test_analyser_pdf_success(mock_service):
    mock_service.return_value = {
        "type_contenu": "probleme",
        "message": "PDF contient un exercice"
    }

    pdf_bytes = create_simple_pdf()

    files = {
        "file": ("test.pdf", io.BytesIO(pdf_bytes), "application/pdf")
    }

    response = client.post("/analyse/analyser_pdf", files=files)

    assert response.status_code == 200
    data = response.json()

    assert data["type_contenu"] == "probleme"
    assert "PDF" in data["message"] or "exercice" in data["message"]
    
    
@pytest.mark.integration
@patch("app.api.agents.comprehension.analyser_pdf_with_trace")
def test_analyser_pdf_rejects_non_pdf(mock_service):
    mock_service.return_value = {
        "type_contenu": "erreur",
        "message": "Le fichier doit être un PDF."
    }

    files = {
        "file": ("test.txt", io.BytesIO(b"hello"), "text/plain")
    }

    response = client.post("/analyse/analyser_pdf", files=files)

    assert response.status_code == 200
    data = response.json()

    assert data["type_contenu"] == "erreur"
    assert "PDF" in data["message"]
    
    
@pytest.mark.integration
@patch("app.api.agents.comprehension.analyser_pdf_with_trace")
def test_analyser_pdf_empty_file(mock_service):
    mock_service.return_value = {
        "type_contenu": "erreur",
        "message": "PDF vide ou invalide"
    }

    files = {
        "file": ("empty.pdf", io.BytesIO(b""), "application/pdf")
    }

    response = client.post("/analyse/analyser_pdf", files=files)

    assert response.status_code == 200
    data = response.json()

    assert "type_contenu" in data
    assert data["type_contenu"] == "erreur"