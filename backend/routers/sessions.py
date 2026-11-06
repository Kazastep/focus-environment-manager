""" Файл sessions с временной логикой и роутем, 
позже переедет в v1/и файлы моделей и роута и логики.
"""
from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse

from backend.pydantic.models import Session
from storage import sessions_db # Временное хранилище

# Роутер сущности
router = APIRouter(prefix="/sessions")

@router.get("", status_code= status.HTTP_200_OK)
async def get_sessions():
    """ Возвращение базу данных сессий. """
    return sessions_db


@router.get("/{session_id}", status_code= status.HTTP_200_OK)
async def get_session(session_id:int):
    """
    Получение сессии по айдишнику.
    С проверкой на существование.
    С конфликтом поднимает 404.
    """
    if session_id not in sessions_db:
        return JSONResponse({}, status_code= status.HTTP_404_NOT_FOUND)
    return sessions_db[session_id]


@router.post("", status_code= status.HTTP_201_CREATED)
async def post_session(session:Session):
    """ 
    Создает сессию без айди, айди присваиваем автоматически внутри ручки
    """
    # Временная генерация ID до перехода на автоинкремент в PostgreSQL.
    # При пустой базе мы присваиваем один, если нет то к максимальному прибавляем один
    if not sessions_db:
        key = 1
    else:
        key = max(sessions_db.keys()) + 1

    session.session_id = key
    sessions_db[key] = session
    return session


@router.put("/{session_id}", status_code= status.HTTP_200_OK)
async def put_session(session_id:int, session:Session):
    """ 
    Изменение сущности по айди с проверкой на существование.
    При ошибке, поднимится 404.
    """
    if session_id not in sessions_db:
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)
    
    session.session_id = session_id
    sessions_db[session_id] = session
    return session


@router.delete("/{session_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_session(session_id:int):
    """ 
    Удаление сессии по айди с проверкой на существование с поднятием 404.
    При успешном удалении вернется 204.
    """
    if session_id not in sessions_db:
        return JSONResponse({}, status_code= status.HTTP_404_NOT_FOUND)
    
    sessions_db.pop(session_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)