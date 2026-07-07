import os
import httpx

IGDB_CLIENT_ID = os.getenv("IGDB_CLIENT_ID", "")
IGDB_CLIENT_SECRET = os.getenv("IGDB_CLIENT_SECRET", "")
GAME_SERVICE_URL = os.getenv("GAME_SERVICE_URL", "http://localhost:8001")

token_cache = {"token": None} # Cacheo de token 

async def get_token_igdb() -> str:
    if token_cache["token"]:
        return token_cache["token"]
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://id.twitch.tv/oauth2/token",
            data={
                "client_id": IGDB_CLIENT_ID,
                "client_secret": IGDB_CLIENT_SECRET,
                "grant_type": "client_credentials"
            }
        )
    response.raise_for_status()
    token_cache["token"] = response.json()["access_token"]
    return token_cache["token"]

async def get_favorite_genre() -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GAME_SERVICE_URL}/games/genres/top")
        response.raise_for_status()
        return response.json()
    
async def genre_recommendation(genres: list[str]) -> list[dict]:
    if not genres:
        return[]
    token = await get_token_igdb()

    headers = {
        "Client-ID": IGDB_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    genre = genres[0]
    body = f'fields name,genres.name,rating,cover.url; where genres.name = "{genre}" & rating > 80; limit 10;' #Query 

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.igdb.com/v4/games",
            headers=headers,
            content=body  # texto plano, no JSON
        )
        response.raise_for_status()
        games = response.json()

    return [
        {
            "title": g.get("name"),
            "rating": g.get("rating"),
            "genres": [genre["name"] for genre in g.get("genres", [])],
            "cover": g.get("cover", {}).get("url")
        }
        for g in games
    ]
