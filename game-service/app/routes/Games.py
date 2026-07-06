from fastapi import APIRouter, Depends, HTTPException
from app.database.Session import getdb
from typing import List
from sqlalchemy.orm import Session
from app.models.Game import Game
from app.schema.Game import GameCreated, GameResponse, GameUpdated

router = APIRouter(prefix="games",
                   tags=["games"])

