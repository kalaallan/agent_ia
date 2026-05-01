from unittest.mock import patch
from app.services.analyse.ai_service import analyser_pdf_gemini

@patch('app.services.analyse.ai_service.call_gemini_with_retry')
@patch('app.services.analyse.ai_service.client.files.upload')
def test_analyser_pdf_gemini_ok(mock_upload, mock_call, fake_pdf_bytes):
    mock_upload.return_value = {
    "name": "files/fake123",
    "uri": "gs://fake-bucket/fake.pdf",
    "mime_type": "application/pdf",
    "state": "ACTIVE"
    }
    mock_call.return_value = '{"type": "information", "raison": "Il n\'y a pas de problème à résoudre."}'
    pdf_bytes = fake_pdf_bytes
    result = analyser_pdf_gemini(pdf_bytes)
    assert result["type_contenu"] in ["information", "probleme"]
    assert result['message'] == "Il n'y a pas de problème à résoudre."
    
    
@patch('app.services.analyse.ai_service.call_gemini_with_retry')
@patch('app.services.analyse.ai_service.client.files.upload')
def test_analyser_pdf_gemini_markdown(mock_upload, mock_call, fake_pdf_bytes):
    mock_upload.return_value = {
    "name": "files/fake123",
    "uri": "gs://fake-bucket/fake.pdf",
    "mime_type": "application/pdf",
    "state": "ACTIVE"
    }
    mock_call.return_value = """```json
    {"type": "probleme", "raison": "Le PDF contient peut-être une question à résoudre."}
    ```"""
    pdf_bytes = fake_pdf_bytes
    result = analyser_pdf_gemini(pdf_bytes)
    assert result["type_contenu"] in ["information", "probleme"]
    assert result['message'] == "Le PDF contient peut-être une question à résoudre."


@patch('app.services.analyse.ai_service.call_gemini_with_retry')
@patch('app.services.analyse.ai_service.client.files.upload')
def test_analyser_pdf_gemini_parsing_error(mock_upload, mock_call, fake_pdf_bytes):
    mock_upload.return_value = {
    "name": "files/fake123",
    "uri": "gs://fake-bucket/fake.pdf",
    "mime_type": "application/pdf",
    "state": "ACTIVE"
    }
    mock_call.return_value = 'Not a JSON response'
    pdf_bytes = fake_pdf_bytes
    result = analyser_pdf_gemini(pdf_bytes)
    assert result['type_contenu'] == 'erreur'
    assert 'Parsing failed' in result['message']