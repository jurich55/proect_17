
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from fastapi import APIRouter, Depends, status, HTTPException, FastAPI

from typing import Annotated
from app.models.m_user import User
from app.schemas import CreateUser, UpdateUser

from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix='/user', tags=['user'])

@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    if users is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no users')
    return users  # возвращаем список всех пользователей из БД
#---------------------------------------------

@router.get('/user_id')
async def user_by_id(user_id: int, db: Annotated[Session,
                     Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")
    return user
#------------------------------------------
# Добавление
@router.post('/create')
async def create_user(user: CreateUser,
        db: Annotated[Session, Depends(get_db)]):

    existing_user = db.scalar(select(User)
        .where(User.username == user.username))
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )
    db.execute(insert(User)
      .values(username=user.username,
              firstname=user.firstname,
              lastname=user.lastname,
              age=user.age,
              slug=slugify(user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful!'}
#----------------------------------------
@router.put('/update')
async def update_user(update_user: UpdateUser, user_id: int,
                db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(update(User).where(User.id == user_id)
      .values(firstname = user.firstname,
              lastname = user.lastname,
              age = user.age))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is Successful!'}
#-------------------------------------------
@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
    db.execute(delete(User).where(User.id == user_id))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful!'}


'''  Создайте, измените и удалите записи через интерфейс Swagger:
Создайте 3 записи User с соответствующими параметрами:
1. username: user1, user2, user3
2. firstname: Pasha, Roza, Alex
3. lastname: Technique, Syabitova, Unknown
3. age: 40, 62, 25
Измените запись с id=3: firstname = Bear, lastname = Grylls, age = 50
Удалите запись с id =2.
Выведите всех пользователей.
Проверьте, выбрасываются ли исключения в ваших запросах.'''