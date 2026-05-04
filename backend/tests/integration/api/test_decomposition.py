import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from ...utils.pdf_factory import create_simple_pdf

client = TestClient(app)


@pytest.mark.integration
@patch("app.services.comprehension.comprehension_langfuse.comprendre_pdf_with_trace")
def test_decomposition_pdf_success(mock_service):

    mock_service.return_value = {
        "conseils": ["Lire attentivement l’énoncé"],
        "prerequis": ["Algebra"],
        "outils": ["Calculatrice"],
        "temps_estime": 30,
        "warning": []
    }

    pdf_bytes = create_simple_pdf()

    files = {
        "file": ("test.pdf", io.BytesIO(pdf_bytes), "application/pdf")
    }

    response = client.post("/comprehension/comprehension_pdf", files=files)

    assert response.status_code == 200

    data = response.json()

    assert "conseils" in data
    assert "prerequis" in data
    assert "outils" in data
    assert "temps_estime" in data
    assert "warning" in data
