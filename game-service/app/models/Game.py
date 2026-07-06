import enum
from sqlalchemy import Integer, Column, String, Enum, Float
from app.database.Session import Base
from app.schema.Game import GameCreated, GameUpdated, GameResponse

class GameStatus(str, enum.Enum):
    jugando = "jugando"
    completado = "completado"
    pendiente = "pendiente"
    abandonado = "abandonado"

class Game(Base):
    __tablename__= "games"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    status = Column(Enum(GameStatus), default=GameStatus.pendiente)
    rating = Column(Float, nullable=True)
    igdb_id = Column(Integer, nullable=True)

