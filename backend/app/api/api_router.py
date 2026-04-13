from fastapi import APIRouter
from app.api.agents import comprehension, decomposition

api_router = APIRouter()

api_router.include_router(
    comprehension.router,
    prefix="/analyse",
    tags=["Agents1"],
)

api_router.include_router(
    decomposition.router,
    prefix="/comprehension",
    tags=["Agents2"],
)
