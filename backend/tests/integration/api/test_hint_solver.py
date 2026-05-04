import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app
from ...utils.pdf_factory import create_simple_pdf

client = TestClient(app)


@pytest.mark.integration
@patch("app.api.agents.hint_solver.process_pdf", new_callable=AsyncMock)
def test_hint_solver_pdf_success(mock_process):
    mock_process.return_value = {
        "type": "hint",
        "message": "Commence par poser une équation simple"
    }

    pdf_bytes = create_simple_pdf()

    files = {
        "file": ("test.pdf", io.BytesIO(pdf_bytes), "application/pdf")
    }

    response = client.post("/hint_solver/hint_solver_pdf", files=files)

    assert response.status_code == 200

    data = response.json()
    assert data["type"] == "hint"
    assert "équation" in data["message"]
    
    
@pytest.mark.integration
def test_hint_solver_pdf_rejects_non_pdf():
    files = {
        "file": ("test.txt", io.BytesIO(b"hello"), "text/plain")
    }

    response = client.post("/hint_solver/hint_solver_pdf", files=files)

    assert response.status_code == 400

    data = response.json()
    assert data["detail"] == "Le fichier doit être un PDF."
    
    
@pytest.mark.integration
@patch("app.api.agents.hint_solver.process_pdf", new_callable=AsyncMock)
def test_hint_solver_pdf_service_error(mock_process):
    mock_process.side_effect = Exception("LLM crash")

    pdf_bytes = create_simple_pdf()

    files = {
        "file": ("test.pdf", io.BytesIO(pdf_bytes), "application/pdf")
    }

    response = client.post("/hint_solver/hint_solver_pdf", files=files)

    assert response.status_code == 500

    data = response.json()
    assert "Erreur lors du traitement" in data["detail"]