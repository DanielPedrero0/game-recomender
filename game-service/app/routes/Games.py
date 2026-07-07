from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.models.Game import Game
from app.schema.Game import GameCreated, GameResponse, GameUpdated
from app.database.Session import getdb

router = APIRouter(prefix="/games",
                   tags=["games"])

def search_game (game_id : int , db : Session) -> Game:
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code = 401, detail = "Juego no encontrado")
    return game

#Añadir un juego
@router.post("/" , response_model = GameResponse , status_code = 201)
async def add_game (game : GameCreated, db : Session = Depends(getdb)):
    db_game = Game(**game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

#Filtrar juegos
@router.post("/", response_model = List[GameResponse])
async def get_games(status : str = None, genre : str = None, db : Session = Depends(getdb)):
    game = db.query(Game)
    if status:
       query = query.filter(Game.status == status)
    if genre: 
        query = query.filter(Game.genre == genre)
    return query.all()
       
#Obtener juego mediante ID
@router.get("/{game_id}" , response_model = GameResponse)
async def get_game_id(game_id : int = None,db : Session = Depends(getdb)):
    return search_game(game_id, db)
    
#Actualizar Juego
@router.patch("/{game_id}" , response_model = GameResponse)
async def update_game(game_id : int , db : Session = Depends (getdb)):
    game = search_game(game_id, db)
    for key,value in update.model_dump(exclude_unset = True).items():
        setattr(game, key, value)
    db.commit()
    db.refresh(game)
    return game


#Eliminar Juego
@router.delete("/{game_id}", status_code = 204)
async def delete_game(game_id : int , db : Session= Depends(getdb)):
    game =  search_game(game_id, db)
    db.delete(game)
    db.commit()


#Obtener todos los juegos
@router.get("/" , response_model=List[GameResponse])
async def get_games(status: str = None , genre : str = None , db : Session = Depends(getdb)):
    query = db.query(Game)
    if status:
        query = query.filter(Game.status == status)
    if genre:
        query = query.filter(Game.genre == genre)
    return query.all()


@router.get("/genres/top", response_model=List[str])
async def get_favourite_genres(db: Session = Depends(getdb)):
    games = db.query(Game).filter(Game.status == "completado").all()
    genres = [g.genre for g in games]
    return sorted(set(genres), key=lambda g: genres.count(g), reverse=True)