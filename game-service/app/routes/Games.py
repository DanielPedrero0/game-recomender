from fastapi import APIRouter, Depends, HTTPException
from database.Session import getdb
from typing import List
from sqlalchemy.orm import Session

router = APIRouter(prefix="games",
                   tags=["games"])

