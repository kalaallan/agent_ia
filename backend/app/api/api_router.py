from fastapi import APIRouter
from app.api.agents import comprehension  # Import de ton fichier agent

api_router = APIRouter()

# On inclut le router de l'agent avec un préfixe et un tag pour la doc
api_router.include_router(
    comprehension.router, prefix="/comprehension", tags=["Agents"]
)
