from fastapi import APIRouter
from app.api.agents import comprehension, decomposition, hint_solver, upload, query

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

api_router.include_router(
    upload.router,
    prefix="/uploads",
    tags=["Upload"],
)

api_router.include_router(
    query.router,
    prefix="/query",
    tags=["Query"],
)