"""
CRUD-эндпоинты для управления событиями активности.

Временная реализация с хранением данных в памяти.
В дальнейшем маршруты и бизнес-логика будут разделены,
а хранение данных перенесено в PostgreSQL.
"""

from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse

from backend.pydantic.models import Event
from storage import events_db


router = APIRouter(prefix="/events")


@router.get("", status_code=status.HTTP_200_OK)
async def get_events():
    """Возвращает все события активности."""
    return events_db


@router.get("/{event_id}", status_code=status.HTTP_200_OK)
async def get_event(event_id: int):
    """
    Возвращает событие по ID.

    Если событие не существует, возвращает HTTP 404.
    """
    if event_id not in events_db:
        return JSONResponse({},status_code=status.HTTP_404_NOT_FOUND)
    return events_db[event_id]


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_event(event: Event):
    """Создаёт новое событие с автоматически назначенным ID."""

    # Временная генерация ID до перехода на автоинкремент в PostgreSQL.
    if not events_db:
        key = 1
    else:
        key = max(events_db.keys()) + 1

    event.event_id = key
    events_db[key] = event

    return event


@router.put("/{event_id}", status_code=status.HTTP_200_OK)
async def put_event(event_id: int, event: Event):
    """
    Обновляет существующее событие по ID.

    Если событие не найдено, возвращает HTTP 404.
    """
    if event_id not in events_db:
        return JSONResponse({},status_code=status.HTTP_404_NOT_FOUND)

    event.event_id = event_id
    events_db[event_id] = event

    return event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int):
    """
    Удаляет событие по ID.

    Возвращает HTTP 204 при успешном удалении
    или HTTP 404, если событие не найдено.
    """
    if event_id not in events_db:
        return JSONResponse({},status_code=status.HTTP_404_NOT_FOUND)

    events_db.pop(event_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)