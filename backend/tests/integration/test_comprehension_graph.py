import pytest
from app.services.comprehension.comprehension_graph import extract_and_detect, langchain_node, gemini_multimodal_node, comprendre_pdf

from tests.utils.pdf_factory import create_simple_pdf


@pytest.mark.integration
def test_extract_and_detect_simple_pdf():

    pdf_bytes = create_simple_pdf()

    state = {"pdf_bytes": pdf_bytes}

    result = extract_and_detect(state)

    assert "text" in result
    assert "is_complex" in result
    
  
@pytest.mark.integration
def test_langchain_node_integration(simple_document):

    state = {
        "text": simple_document
    }

    result = langchain_node(state)

    assert "result" in result
    assert "source" in result

    assert isinstance(result["result"], dict)

    assert (
        "conseils" in result["result"]
        or "erreur" in result["result"]
    )

    assert result["source"].startswith("groq:")
    
    
@pytest.mark.integration
def test_gemini_multimodal_node_integration():

    pdf_bytes = create_simple_pdf()
    state = {"pdf_bytes": pdf_bytes}

    result = gemini_multimodal_node(state)

    assert "result" in result
    assert "source" in result

    assert result["source"] == "gemini"

    assert isinstance(result["result"], dict)

    assert (
        "conseils" in result["result"]
        or "erreur" in result["result"]
    )
    
    
@pytest.mark.e2e
def test_comprendre_pdf_integration():

    pdf_bytes = create_simple_pdf()

    result = comprendre_pdf(pdf_bytes)

    assert isinstance(result, dict)

    assert (
        "conseils" in result
        or "erreur" in result
    )
    
