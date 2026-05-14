from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ragEnd.rag_end import search_in_pdf

router = APIRouter()


class SearchRequest(BaseModel):
    user_query: str
    file_id: str


@router.post("/query_pdf")
async def search_pdf(data: SearchRequest):

    results = search_in_pdf(
        user_query=data.user_query,
        file_id=data.file_id
    )

    return results