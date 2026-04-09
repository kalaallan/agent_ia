from fastapi import APIRouter, UploadFile, File
from app.models.schemas import PDFResponse
from app.services.langfuse_client import analyser_pdf_with_trace

router = APIRouter()


@router.post("/analyser_pdf", response_model=PDFResponse)
async def analyser_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return PDFResponse(
            type_contenu="erreur", message="Le fichier doit être un PDF."
        )

    pdf_bytes = await file.read()
    resultat = analyser_pdf_with_trace(pdf_bytes, file.filename)
    return resultat
