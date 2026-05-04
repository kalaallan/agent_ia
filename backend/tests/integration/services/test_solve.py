import pytest

from app.services.indice.pipeline.solver import process_document


@pytest.mark.integration
def test_process_document_real(fake_pdf_bytes):

    file_bytes = fake_pdf_bytes

    result = process_document(file_bytes, max_iterations=2)

    assert isinstance(result, list)

    if len(result) > 0:
        exercise = result[0]

        assert "solution" in exercise
        assert "hint" in exercise
        assert "type" in exercise