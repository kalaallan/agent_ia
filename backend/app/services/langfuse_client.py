from app.utils.langfuse_utils import langfuse_client
from app.services.ai_service import analyser_pdf_gemini


def analyser_pdf_with_trace(
    pdf_bytes: bytes, filename: str, user_id: str = "anonymous"
):
    # On utilise start_as_current_observation() sur le client Langfuse
    with langfuse_client.start_as_current_observation(
        name="analyse_pdf",
        input={"filename": filename},
        metadata={"user_id": user_id},
    ) as span:
        try:
            # Exécution de l'IA
            resultat = analyser_pdf_gemini(pdf_bytes)

            # On prépare un dictionnaire simple pour Langfuse
            output_data = {
                "type_contenu": resultat.get("type_contenu"),
                "message": resultat.get("message"),
            }

            # UPDATE avec des données propres
            span.update(output=output_data)
            return resultat

        except Exception as e:
            # Capture de l'erreur dans la trace
            span.update(level="ERROR", status_message=str(e))
            raise e
