from app.backend.db import SessionLocal
from fastapi import Depends
from app.backend.db import SessionLocal

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()