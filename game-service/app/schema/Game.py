from app.models.Game import GameStatus
from pydantic import BaseModel, Field
from typing import Optional
class GameCreated(BaseModel):
    title : str
    genre : str
    platform : str
    status : GameStatus =  GameStatus.pendiente
    rating : Optional[float] = Field(None, ge=1 , le=10)
    igdb_id : Optional[int] = None

class GameUpdated(BaseModel):
    status : Optional[GameStatus] = None
    rating: Optional[float] = Field(None, ge=1, le=10)

class GameResponse(BaseModel):
    id : int
    
    class Config:
        from_attributes = True