from fastapi import FastAPI
from app.api.api_router import api_router

app = FastAPI(title="AI Coach API")

# On branche le hub de routes
app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API AI Coach"}
