from fastapi import FastAPI
from app.routers import task
from app.routers import user

from app.backend.db import engine, Base
app = FastAPI()

@app.get('/')
async def welcome():
    return {"message": "Welcome to taskmanager database"}

# Подключаем роутеры
app.include_router(user.router)
app.include_router(task.router)


#   alembic revision --autogenerate -m "Initial migration"

#   uvicorn app.main:app --reload
#   http://127.0.0.1:8000
#   http://127.0.0.1:8000/docs

#   pip install -U python-slugify
#  python -m pip install --upgrade pip