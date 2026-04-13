from fastapi import FastAPI
from app.api.api_router import api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI Coach API")

# On branche le hub de routes
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API AI Coach"}
