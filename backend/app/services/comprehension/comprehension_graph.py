# services/comprehension_graph.py

from typing import TypedDict
from app.services.comprehension.comprehension_service import run_chain_with_fallback
from app.utils.gemini_utils import client, call_gemini_with_retry
from langgraph.graph import StateGraph, END
from app.utils.langfuse_graph import LangfuseGraphTrace
from app.utils.langfuse_utils import langfuse_client

import json
import io
import pdfplumber


# ----------------------------
# STATE
# ----------------------------
class GraphState(TypedDict, total=False):
    pdf_bytes: bytes
    text: str
    is_complex: bool
    result: dict
    source: str


def extract_and_detect(state: GraphState):

    with langfuse_client.start_as_current_observation(
        name="extract_and_detect",
        input={"size": len(state["pdf_bytes"])}
    ) as span:

        text = ""
        has_tables = False
        has_images = False

        with pdfplumber.open(io.BytesIO(state["pdf_bytes"])) as pdf:
            for page in pdf.pages:

                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

                if page.extract_tables():
                    has_tables = True

                if getattr(page, "images", []):
                    has_images = True

        text = text.strip()

        complexity_score = 0
        if has_tables:
            complexity_score += 1
        if has_images:
            complexity_score += 1

        keywords = ["figure", "graph", "diagramme", "schéma", "tableau", "courbe"]
        if any(k in text.lower() for k in keywords):
            complexity_score += 1

        is_complex = complexity_score >= 2

        output = {
            "text": text,
            "is_complex": is_complex,
        }

        span.update(output=output)

        return {**state, **output}


def langchain_node(state: GraphState):

    with langfuse_client.start_as_current_observation(
        name="langchain_node",
        input={"text_length": len(state.get("text", ""))}
    ) as span:

        try:
            result = run_chain_with_fallback(state.get("text", ""))

            output = {
                "result": result["result"],
                "source": result["source"],
            }

            span.update(output=output)

            return {**state, **output}

        except Exception as e:

            span.update(level="ERROR", status_message=str(e))

            return {
                **state,
                "result": {"erreur": "langchain_failed"},
                "source": "langchain"
            }


def gemini_multimodal_node(state: GraphState):

    with langfuse_client.start_as_current_observation(
        name="gemini_multimodal_node",
        input={"has_pdf": True}
    ) as span:

        uploaded_file = client.files.upload(
            file=io.BytesIO(state["pdf_bytes"]),
            config={
                "mime_type": "application/pdf",
                "display_name": "document.pdf",
            },
        )

        prompt = """
Tu es un expert pédagogique.

Retourne STRICTEMENT du JSON :

{
  "conseils": [],
  "prerequis": [],
  "outils": [],
  "temps_estime": 0,
  "warning": ["Gemini"]
}
"""

        txt = call_gemini_with_retry(uploaded_file, prompt)

        try:
            data = json.loads(txt)

            output = {
                "result": data,
                "source": "gemini"
            }

            span.update(output=output)

            return {**state, **output}

        except Exception as e:

            span.update(level="ERROR", status_message=str(e))

            return {
                **state,
                "result": {"erreur": "Parsing failed", "raw": txt},
                "source": "gemini"
            }


def router(state: GraphState):

    if state.get("is_complex", False):
        return "gemini"

    return "langchain"


def check_quality(state: GraphState):

    result = state.get("result") or {}

    if "erreur" in result:
        return "retry_with_vision"

    if not result.get("conseils"):
        return "retry_with_vision"

    return "finish"


def check_final_result(state: GraphState):

    result = state.get("result") or {}

    if "erreur" in result:
        return "fail"

    if not result.get("conseils"):
        return "fail"

    return "success"


def guardrails_node(state: GraphState):

    with langfuse_client.start_as_current_observation(
        name="guardrails_node",
        input=state.get("result", {})
    ) as span:

        output = {
            "conseils": ["Relire l'énoncé attentivement"],
            "prerequis": ["Compréhension de base du sujet"],
            "outils": ["Papier", "Stylo"],
            "temps_estime": 30,
            "warning": ["Garde_fous"]
        }

        span.update(output=output)

        return {**state, "result": output}


graph = StateGraph(GraphState)

graph.add_node("extract", extract_and_detect)
graph.add_node("langchain", langchain_node)
graph.add_node("gemini", gemini_multimodal_node)
graph.add_node("guardrails", guardrails_node)

graph.set_entry_point("extract")

graph.add_conditional_edges(
    "extract",
    router,
    {"langchain": "langchain", "gemini": "gemini"},
)

graph.add_conditional_edges(
    "langchain",
    check_quality,
    {"retry_with_vision": "gemini", "finish": END},
)

graph.add_conditional_edges(
    "gemini",
    check_final_result,
    {"success": END, "fail": "guardrails"},
)

graph.add_edge("guardrails", END)

app = graph.compile()


def comprendre_pdf(pdf_bytes: bytes):

    with LangfuseGraphTrace("comprehension_pdf") as trace:

        result = app.invoke({"pdf_bytes": pdf_bytes})

        trace.update(output={"result": result.get("result")})

        return result.get("result", {})
