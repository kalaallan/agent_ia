from fastapi import APIRouter

# On crée un router spécifique pour cet agent
router = APIRouter()


@router.get("/test")
def test_comprehension():
    return {"status": "Agent de compréhension opérationnel"}
