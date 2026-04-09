from pydantic import BaseModel


class PDFResponse(BaseModel):
    type_contenu: str  # "probleme" ou "information"
    message: str  # message explicatif
