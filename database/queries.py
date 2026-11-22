"""Функции для работы с базой данных (CRUD)."""

from datetime import datetime, date, time
from sqlalchemy import insert, select, update, and_
from database.database import async_session_factory
from database.models import users_table, sessions_table, event_table


async def ensure_default_user() -> int:
    """Создаёт локального пользователя для MVP (так как авторизации пока нет)."""
    async with async_session_factory() as session:
        # Проверяем, есть ли уже пользователь
        query = select(users_table.c.user_id).where(
            users_table.c.user_name == "local_user"
        )
        res = await session.execute(query)
        user_id = res.scalar_one_or_none()

        if user_id is None:
            # Создаём, если нет
            stmt = (
                insert(users_table)
                .values(
                    user_name="local_user",
                    user_email="local@fem.app",
                    password_hash="local_mvp_no_auth",
                )
                .returning(users_table.c.user_id)
            )
            res = await session.execute(stmt)
            user_id = res.scalar_one()
            await session.commit()

        return user_id


async def start_session(user_id: int, started_at: datetime | None = None) -> int:
    """Открывает новую рабочую сессию и возвращает её ID."""
    started_at = started_at or datetime.now()
    async with async_session_factory() as session:
        stmt = (
            insert(sessions_table)
            .values(user_id=user_id, started_at=started_at)
            .returning(sessions_table.c.session_id)
        )
        res = await session.execute(stmt)
        await session.commit()
        return res.scalar_one()


async def end_session(session_id: int, ended_at: datetime | None = None) -> None:
    """Закрывает рабочую сессию."""
    ended_at = ended_at or datetime.now()
    async with async_session_factory() as session:
        stmt = (
            update(sessions_table)
            .where(sessions_table.c.session_id == session_id)
            .values(ended_at=ended_at)
        )
        await session.execute(stmt)
        await session.commit()


async def insert_events(events_data: list[dict]) -> None:
    """
    Массовая вставка сырых событий от агента в базу.
    Ожидается список словарей:
    [{"session_id": 1, "timestamp": dt, "app": "Code.exe", "window_title": "main.py", "state": "active", "duration": 5}]
    """
    if not events_data:
        return
    async with async_session_factory() as session:
        stmt = insert(event_table).values(events_data)
        await session.execute(stmt)
        await session.commit()


async def get_events_for_date(user_id: int, target_date: date) -> list[dict]:
    """Выгружает все события пользователя за конкретный день (нужно для модуля аналитики)."""
    day_start = datetime.combine(target_date, time.min)
    day_end = datetime.combine(target_date, time.max)

    async with async_session_factory() as session:
        query = (
            select(
                event_table.c.event_id,
                event_table.c.session_id,
                event_table.c.timestamp,
                event_table.c.app,
                event_table.c.window_title,
                event_table.c.state,
                event_table.c.duration,
            )
            .select_from(
                event_table.join(
                    sessions_table,
                    event_table.c.session_id == sessions_table.c.session_id,
                )
            )
            .where(
                and_(
                    sessions_table.c.user_id == user_id,
                    event_table.c.timestamp >= day_start,
                    event_table.c.timestamp <= day_end,
                )
            )
            # Обязательно сортируем по времени, чтобы правильно считать переключения
            .order_by(event_table.c.session_id, event_table.c.timestamp.asc())
        )
        res = await session.execute(query)
        # Возвращаем список словарей для удобной работы в аналитике
        return [dict(row._mapping) for row in res.all()]
