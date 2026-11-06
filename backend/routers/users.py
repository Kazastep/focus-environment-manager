""" Файл users с временной логикой и роутем, 
позже переедет в v1/и файлы моделей и роута и логики.
"""
from fastapi import APIRouter, status, Response, HTTPException
from fastapi.responses import JSONResponse

from backend.pydantic.models import User
from storage import users_db # Временное хранилище

# Роутер сущности
router = APIRouter(prefix="/users")

# Ручка get получает всех юзеров
@router.get("", status_code=status.HTTP_200_OK)
async def get_users():
    """Возвращает список пользователей."""
    return users_db


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    """Возвращает пользователя по ID или ошибку 404."""
    # Проверка на существование
    if user_id not in users_db:
        return JSONResponse({},status_code=status.HTTP_404_NOT_FOUND)
    return users_db[user_id]


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_user(user: User):
    """
    Создаёт пользователя с автоматически назначенным ID.
    Проверяет уникальность имени и электронной почты.
    При конфликте возвращает ошибку 409.
    """
    # Временная генерация ID до перехода на автоинкремент в PostgreSQL.
    # Если юзера нет то ключ один, если есть то к max прибавляем один.
    if not users_db:
        key = 1
    else:
        key = max(users_db.keys()) + 1

    # Проверка на уникальность почты и имени
    for existing_user in users_db.values():
        if existing_user.user_email == user.user_email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Почта занята")

        if existing_user.user_name == user.user_name:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Имя занято")
        
    user.user_id = key
    users_db[key] = user
    return user


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def put_user(user_id: int, user: User):
    """ 
    Изменяет юзера по айди.
    Проверяет существование. При конфликте возвращает 404.
    """
    # Проверка на существование
    if user_id not in users_db:
        return JSONResponse({},status_code=status.HTTP_404_NOT_FOUND)

    user.user_id = user_id
    users_db[user_id] = user

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """ 
    Удаление юзера по айди.
    Проверка на существование.
    Приконфликте 404.
    """
    # Проверка на существование
    if user_id not in users_db:
        return JSONResponse({},status_code=status.HTTP_404_NOT_FOUND)

    users_db.pop(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)