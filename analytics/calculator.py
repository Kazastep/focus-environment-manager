"""Модуль аналитики: расчёт статистики и продуктивности по сырым данным."""

from collections import defaultdict
from datetime import date
from sqlalchemy.dialects.postgresql import insert as pg_insert

from database.database import async_session_factory
from database.models import statistics_table
from database.queries import get_events_for_date


async def calculate_and_save_daily_stats(user_id: int, target_date: date) -> dict:
    """
    Выгружает события за день, рассчитывает метрики MVP (время, переключения, приложения)
    и сохраняет/обновляет их в таблице statistics.
    """
    events = await get_events_for_date(user_id, target_date)

    if not events:
        # Если событий нет, сохраняем нулевую статистику
        empty_stat = {
            "user_id": user_id,
            "statistics_date": target_date,
            "total_focus_time": 0,
            "total_idle_time": 0,
            "idle_ratio": 0.0,
            "context_switches": 0,
            "top_apps": {},
            "session_count": 0,
        }
        await upsert_daily_statistics(empty_stat)
        return empty_stat

    total_focus_time = 0
    total_idle_time = 0
    context_switches = 0
    app_durations: dict[str, int] = defaultdict(int)
    unique_sessions = set()

    prev_app = None
    prev_session_id = None

    for ev in events:
        session_id = ev["session_id"]
        unique_sessions.add(session_id)

        duration = ev.get("duration", 1)
        state = ev.get("state", "active")
        app = ev["app"]

        if state == "idle":
            total_idle_time += duration
        else:
            total_focus_time += duration
            app_durations[app] += duration

            # Считаем переключение контекста, если сменилось активное приложение внутри одной сессии
            if (
                prev_session_id == session_id
                and prev_app is not None
                and prev_app != app
            ):
                context_switches += 1

            prev_app = app
            prev_session_id = session_id

    total_time = total_focus_time + total_idle_time
    idle_ratio = round(total_idle_time / total_time, 4) if total_time > 0 else 0.0

    # Сортируем словарь приложений по убыванию времени
    sorted_top_apps = dict(
        sorted(app_durations.items(), key=lambda item: item[1], reverse=True)
    )

    stat_payload = {
        "user_id": user_id,
        "statistics_date": target_date,
        "total_focus_time": total_focus_time,
        "total_idle_time": total_idle_time,
        "idle_ratio": idle_ratio,
        "context_switches": context_switches,
        "top_apps": sorted_top_apps,
        "session_count": len(unique_sessions),
    }

    await upsert_daily_statistics(stat_payload)
    return stat_payload


async def upsert_daily_statistics(stat_data: dict) -> None:
    """Вспомогательная функция: сохраняет или обновляет рассчитанную статистику за день (UPSERT)."""
    async with async_session_factory() as session:
        stmt = pg_insert(statistics_table).values(**stat_data)

        # Если статистика за этот день для этого юзера уже есть, просто обновляем поля
        stmt = stmt.on_conflict_do_update(
            constraint="uq_user_stat_date",
            set_={
                "total_focus_time": stmt.excluded.total_focus_time,
                "total_idle_time": stmt.excluded.total_idle_time,
                "idle_ratio": stmt.excluded.idle_ratio,
                "context_switches": stmt.excluded.context_switches,
                "top_apps": stmt.excluded.top_apps,
                "session_count": stmt.excluded.session_count,
            },
        )
        await session.execute(stmt)
        await session.commit()
