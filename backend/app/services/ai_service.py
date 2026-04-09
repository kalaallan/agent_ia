import io
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=API_KEY)


def analyser_pdf_gemini(pdf_bytes: bytes) -> dict:
    uploaded_file = client.files.upload(
        file=io.BytesIO(pdf_bytes),
        config={"mime_type": "application/pdf", "display_name": "document.pdf"},
    )

    # Prompt avec instruction de réponse fixe pour les informations
    prompt = (
        "Agis en tant qu'analyseur de documents. "
        "Détermine si le PDF contient un 'probleme' à résoudre ou est une simple 'information'.\n\n"
        "RÈGLES STRICTES :\n"
        "1. Si le type est 'information', la raison DOIT ÊTRE EXACTEMENT : 'Il n'y a pas de problème à résoudre.'\n"
        "2. Si le type est 'probleme', explique brièvement pourquoi dans la raison.\n"
        "3. Réponds uniquement en JSON."
        'Exemple de réponse JSON : {"type": "information", "raison": "Il n\'y a pas de problème à résoudre."} '
    )

    # Appel avec configuration JSON native
    response = client.models.generate_content(
        model="gemini-2.5-flash",  # Ou gemini-3-flash
        contents=[uploaded_file, prompt],
        config={
            "response_mime_type": "application/json",
        },
    )

    txt = response.text.strip()
    try:
        import json

        data = json.loads(txt)
        return {
            "type_contenu": data.get("type"),
            "message": data.get("raison"),
        }
    except Exception as e:
        if "```json" in txt:
            txt = txt.replace("```json", "").replace("```", "").strip()
            data = json.loads(txt)
            return {"type_contenu": data.get("type"), "message": data.get("raison")}

        return {"type_contenu": "erreur", "message": f"Parsing failed: {e}"}
