import os
import pytest
import io

from unittest.mock import patch, MagicMock
from app.utils.gemini_utils import get_gemini_models, call_gemini_with_retry, call_gemini_multimodal, client
from ...utils.pdf_factory import create_simple_pdf


pytestmark = pytest.mark.skipif(
    not os.getenv("GOOGLE_API_KEY"),
    reason="GOOGLE_API_KEY not set"
)


@pytest.mark.integration
def test_get_gemini_models_real():
    models = get_gemini_models()

    assert isinstance(models, list)
    assert len(models) > 0

    assert all("gemini" in m for m in models)

    if any("flash" in m for m in models):
        assert "flash" in models[0]
        


@pytest.mark.integration
@patch("app.utils.gemini_utils.call_gemini_with_retry")
@patch("app.utils.gemini_utils.client")
def test_call_gemini_with_retry_real(mock_client, mock_call):
    prompt = 'Return JSON: {"message": "hello"}'

    file_bytes = create_simple_pdf()

    mock_uploaded_file = MagicMock()
    mock_client.files.upload.return_value = mock_uploaded_file

    mock_call.return_value = '{"message": "hello"}'

    uploaded_file = mock_client.files.upload(
        file=io.BytesIO(file_bytes),
        config={
            "mime_type": "application/pdf",
            "display_name": "document.pdf",
        },
    )

    response = mock_call(uploaded_file, prompt)

    assert response is not None
    assert "hello" in response.lower()
    

@pytest.mark.integration
def test_call_gemini_multimodal_real():

    prompt = "Explain the content of the document in JSON with key 'answer'"

    file_bytes = create_simple_pdf()

    response = call_gemini_multimodal(file_bytes, prompt)

    assert response is not None
    assert "answer" in response.lower()