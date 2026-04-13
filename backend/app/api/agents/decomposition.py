from fastapi import APIRouter, UploadFile, File
from app.models.comprehension_schema import AnalysePedagogique
from app.services.comprehension.comprehension_langfuse import comprendre_pdf_with_trace

router = APIRouter()


@router.post("/comprehension_pdf", response_model=AnalysePedagogique)
async def analyser_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return AnalysePedagogique(
            type_contenu="erreur", message="Le fichier doit être un PDF."
        )

    pdf_bytes = await file.read()
    resultat = comprendre_pdf_with_trace(pdf_bytes, file.filename)
    return resultat
