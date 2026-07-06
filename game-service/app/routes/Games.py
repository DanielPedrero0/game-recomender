from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.models.Game import Game
from app.schema.Game import GameCreated, GameResponse, GameUpdated
from app.database.Session import getdb

router = APIRouter(prefix="games",
                   tags=["games"])

#Añadir un juego
@router.post("/" , response_model = GameResponse , status_code = 201)
def add_game (game : GameCreated, db : Session = Depends(getdb)):
    db_game = Game(**game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

#Filtrar juegos
@router.post("/", response_model = List[GameResponse])
def get_games(status : str = None, genre : str = None, db : Session = Depends(getdb)):
    game = db.query(Game)
    if status:
       query = query.filter(Game.status == status)
    if genre: 
        query = query.filter(Game.genre == genre)
    return query.all()
       
#Obtener juego mediante ID
@router.get("/{game_id}" , response_model = GameResponse)
def get_game_id(game_id : int = None, db : Session = Depends(getdb)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code = 401, detail = "Juego no encontrado")
    else:
        return game
    
#Actualizar Juego
@router.patch("/{game_id}" , response_model = GameResponse)
def update_game(game_id : int , db : Session = Depends (getdb)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code = 401, detail = "Juego no encontrado")
    for key,value in update.model_dump(exclude_unset = True).items():
        setattr(game, key, value)
    db.commit()
    db.refresh(game)
    return game

#Eliminar Juego
@router.delete("/{game_id}", status_code = 204)
def delete_game(game_id : int , db : Session= Depends(getdb)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code = 401, detail = "Juego no encontrado")
    db.delete(game)
    db.commit()


def search_game (game_id : int , db : Session = Depends(getdb)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code = 401, detail = "Juego no encontrado")
