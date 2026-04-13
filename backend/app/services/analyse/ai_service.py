import io
import json
from app.utils.gemini_utils import client, call_gemini_with_retry

# fallback models (du plus rapide au plus stable)
GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-1.5-flash",
]


def analyser_pdf_gemini(pdf_bytes: bytes) -> dict:
    uploaded_file = client.files.upload(
        file=io.BytesIO(pdf_bytes),
        config={
            "mime_type": "application/pdf",
            "display_name": "document.pdf",
        },
    )

    prompt = (
        "Agis en tant qu'analyseur de documents. "
        "Détermine si le PDF contient un 'probleme' à résoudre ou est une simple 'information'.\n\n"
        "RÈGLES STRICTES :\n"
        "1. Si le type est 'information', la raison DOIT ÊTRE EXACTEMENT : 'Il n'y a pas de problème à résoudre.'\n"
        "2. Si le type est 'probleme', explique brièvement pourquoi dans la raison.\n"
        "3. Réponds uniquement en JSON.\n\n"
        'Exemple : {"type": "information", "raison": "Il n\'y a pas de problème à résoudre."}'
    )

    txt = call_gemini_with_retry(uploaded_file, prompt)

    txt = txt.strip()

    try:
        data = json.loads(txt)
        return {
            "type_contenu": data.get("type"),
            "message": data.get("raison"),
        }

    except Exception as e:
        # fallback si Gemini ajoute des fences markdown
        if "```json" in txt:
            txt = txt.replace("```json", "").replace("```", "").strip()
            data = json.loads(txt)
            return {
                "type_contenu": data.get("type"),
                "message": data.get("raison"),
            }

        return {
            "type_contenu": "erreur",
            "message": f"Parsing failed: {e}",
        }
