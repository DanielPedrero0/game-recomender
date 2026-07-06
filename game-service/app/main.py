from fastapi import FastAPI
from app.database.Session import engine, Base
from app.routes import games

# Crea las tablas en PostgreSQL al arrancar si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(games.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "game-service"}