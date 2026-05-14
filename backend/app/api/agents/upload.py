from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.chargement.upload_service import handle_upload

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Fichier non PDF")

    file_bytes = await file.read()

    file_id = handle_upload(file_bytes)

    return file_id