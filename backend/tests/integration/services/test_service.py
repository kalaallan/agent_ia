import pytest

from app.services.indice.service import process_pdf
from ...utils.pdf_factory import create_simple_pdf


@pytest.mark.integration
@pytest.mark.asyncio
async def test_service():
    # Simulate a PDF file as bytes
    fake_pdf_bytes = create_simple_pdf()

    result = await process_pdf(fake_pdf_bytes)

    assert "meta" in result
    assert "results" in result
