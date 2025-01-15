from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from sqlalchemy import Column, Integer, String
                                      # создаем движок для связи с БД
engine = create_engine("sqlite:///taskmanager.db", echo = True)

SessionLocal = sessionmaker(bind=engine)  # создаем сессию связи с БД

class Base(DeclarativeBase):
    pass