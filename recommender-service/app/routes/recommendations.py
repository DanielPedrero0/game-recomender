from fastapi import APIRouter
from app.services.igdb import get_favorite_genre, genre_recommendation

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)


@router.get("/")
async def get_recommendation():
    try:
        genres = await get_favorite_genre()
    except Exception:
        genres = []

    if not genres:
        return {
            "message": "Aun no tienes juegos completados.",
            "based_on_genres": [],
            "recommendations": []
        }

    try:
        recommendation = await genre_recommendation(genres)
    except Exception:
        recommendation = []

    return {
        "based_on_genres": genres,
        "recommendations": recommendation
    }


@router.get("/health")
async def get_status():
    return {
        "status": "ok",
        "service": "recommender-service"
    }