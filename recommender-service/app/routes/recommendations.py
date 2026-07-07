from fastapi import APIRouter, HTTPException
from app.services.igdb import get_favorite_genre, genre_recommendation, fetch_recommendations

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)


@router.get("/")
async def get_recommendation(genre:str = None):
    try:
        genres = await get_favorite_genre()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"No se pudo conectar con game-service: {str(e)}")

    if not genres:
        return {
            "message": "Aún no tienes juegos completados.",
            "recommendations": []
        }

    
    genre_to_use = [genre] if genre else genres

    recommendations = await fetch_recommendations(genre_to_use)

    return {
        "based_on_genres": genre_to_use,
        "recommendations": recommendations
    }


@router.get("/health")
async def get_status():
    return {
        "status": "ok",
        "service": "recommender-service"
    }