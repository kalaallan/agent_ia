from fastapi import APIRouter
from app.api.agents import comprehension, decomposition, hint_solver

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

api_router.include_router(
    hint_solver.router,
    prefix="/hint_solver",
    tags=["Agents3"],
)
