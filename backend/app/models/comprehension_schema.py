# services/schemas.py

from pydantic import BaseModel


class AnalysePedagogique(BaseModel):
    conseils: list[str]
    prerequis: list[str]
    outils: list[str]
    temps_estime: int
    warning: list[str]
