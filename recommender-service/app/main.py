from fastapi import FastAPI
from app.routes import recommendations

app = FastAPI()


app.include_router(recommendations.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "recommender-service"}