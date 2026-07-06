import enum
from pydantic import BaseModel, Field
from typing import Optional

#Estado de los juegos
class GameStatus(str, enum.Enum):
    jugando = "jugando"
    completado = "completado"
    pendiente = "pendiente"
    abandonado = "abandonado"

#Tabla de juegos
class GameCreated(BaseModel):
    title : str
    genre : str
    platform : str
    status : GameStatus =  GameStatus.pendiente
    rating : Optional[float] = Field(None, ge=1 , le=10)
    igdb_id : Optional[int] = None
#Actualización de juegos
class GameUpdated(BaseModel):
    status : Optional[GameStatus] = None
    rating: Optional[float] = Field(None, ge=1, le=10)
#Respuesta de juegos
class GameResponse(BaseModel):
    id : int
    
    class Config:
        from_attributes = True
