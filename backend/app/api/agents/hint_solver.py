from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.indice.service import process_pdf

router = APIRouter()


@router.post("/hint_solver_pdf")
async def hint_solver_pdf(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Le fichier doit être un PDF."
        )

    try:
        pdf_bytes = await file.read()

        resultat = await process_pdf(pdf_bytes)

        return resultat

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement : {str(e)}"
        )
