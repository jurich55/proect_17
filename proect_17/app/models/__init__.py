from app.models.m_user import User
from app.models.m_task import Task


from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))

from sqlalchemy.schema import CreateTable
print(CreateTable(User.__table__))