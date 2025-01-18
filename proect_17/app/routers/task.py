
from fastapi import APIRouter, Depends, status, HTTPException
from select import select
from sqlalchemy.orm import Session
from unicodedata import category

from app.backend.db_depends import get_db
from typing import Annotated
from app.models import *
from app.schemas import UpdateTask, CreateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    if tasks is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no users')
    else:
        return tasks
#---------------------------------------

@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    else:
        return task

@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)],
                      task: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")
    else:

        db.execute(insert(Task).values(title = task.title,
                                   content = task.content,
                                   priority = task.priority,
                                   user_id = user_id,
                                   slug = slugify(task.title)))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Task create is successful!'}


@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int, task: UpdateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")
    else:
        db.execute(update(Task).where(Task.id == task_id).values(
        title = task.title,
        content = task.content,
        priority = task.priority))
    
        db.commit()
        return  {'status_code': status.HTTP_200_OK,
             'transaction': 'Task update is successful!'}

@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    else:
        db.execute(delete(Task).where(Task.id == task_id))

        db.commit()
        return {'status_code': status.HTTP_200_OK,
            'transaction': 'Task delete is successful!'}


'''  Создайте, измените и удалите записи через интерфейс Swagger:
Создайте 4 записи Task для User с id=1 и id=3, по 2 на каждого в соответствии с порядком ниже:
1. title: FirstTask, SecondTask, ThirdTask, FourthTask
2. content: Content1, Content2, Content3, Content4
3. priority: 0, 2, 4, 6
4. user_id: 1, 1, 3, 3'''
