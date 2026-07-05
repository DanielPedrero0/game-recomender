import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://gameuser:gamepass@localhost:5432/gamedb")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def getdb():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()