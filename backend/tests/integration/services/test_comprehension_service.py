import pytest
from app.services.comprehension.comprehension_service import run_chain_with_fallback


@pytest.mark.integration
def test_run_chain_with_fallback_real(simple_document):

    result = run_chain_with_fallback(simple_document)

    assert "result" in result
    assert "source" in result

    assert isinstance(result["result"], dict)

    assert (
        "conseils" in result["result"]
        or "erreur" in result["result"]
    )

    assert (
        result["source"].startswith("groq:")
        or result["source"] == "groq_failed"
    )