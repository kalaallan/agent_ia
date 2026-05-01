from app.services.comprehension.comprehension_graph import (router, check_quality, check_final_result, guardrails_node)

def test_router():

    state = {"is_complex": True}
    assert router(state) == "gemini"

    state = {"is_complex": False}
    assert router(state) == "langchain"



def test_check_quality():

    state = {"result": {"erreur": "Some error"}}
    assert check_quality(state) == "retry_with_vision"

    state = {"result": {"conseils": []}}
    assert check_quality(state) == "retry_with_vision"

    state = {"result": {"conseils": ["Conseil 1"]}}
    assert check_quality(state) == "finish"


def check_final_result():
    state = {"result": {"erreur": "Some error"}}
    assert check_final_result(state) == "fail"

    state = {"result": {"conseils": []}}
    assert check_final_result(state) == "fail"

    state = {"result": {"conseils": ["Conseil 1"]}}
    assert check_final_result(state) == "success"


def guadrails_node():
    state = {"result": {}}
    new_state = guardrails_node(state)
    assert "conseils" in new_state["result"]
    assert "prerequis" in new_state["result"]
    assert "outils" in new_state["result"]
    assert "temps_estime" in new_state["result"]
    assert "warning" in new_state["result"]
