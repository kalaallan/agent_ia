from app.utils.langfuse_utils import langfuse_client
from app.services.comprehension.comprehension_graph import comprendre_pdf


def comprendre_pdf_with_trace(pdf_bytes: bytes, filename: str, user_id: str = "anonymous"):

    with langfuse_client.start_as_current_observation(
        name="comprehension_pdf",
        input={"filename": filename},
        metadata={"user_id": user_id},
    ) as span:

        try:
            result = comprendre_pdf(pdf_bytes)

            # On extrait des infos utiles
            output_data = {
                "has_error": "erreur" in result,
                "source": result.get("source"),
                "has_warning": "warning" in result,
                "nb_conseils": len(result.get("conseils", [])) if isinstance(result.get("conseils"), list) else 0
            }

            span.update(output=output_data)

            return result

        except Exception as e:
            span.update(level="ERROR", status_message=str(e))
            raise e
