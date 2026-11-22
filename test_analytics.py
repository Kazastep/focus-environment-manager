"""Скрипт для тестирования базы данных и модуля аналитики."""

import asyncio
from datetime import datetime, timedelta
from database.queries import (
    ensure_default_user,
    start_session,
    end_session,
    insert_events,
)
from analytics.calculator import calculate_and_save_daily_stats


async def main():
    print("1. Создаем пользователя (если его нет)...")
    user_id = await ensure_default_user()

    print("2. Открываем тестовую сессию...")
    # Устанавливаем время начала сессии
    start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    session_id = await start_session(user_id, started_at=start_time)

    print("3. Генерируем события (events)...")
    events_data = [
        # 10 минут работы в VS Code (active)
        {
            "session_id": session_id,
            "timestamp": start_time,
            "app": "Code.exe",
            "window_title": "models.py - VS Code",
            "state": "active",
            "duration": 600,
        },
        # Переключение на Chrome на 5 минут (считаем 1-е переключение)
        {
            "session_id": session_id,
            "timestamp": start_time + timedelta(minutes=10),
            "app": "chrome.exe",
            "window_title": "GitHub",
            "state": "active",
            "duration": 300,
        },
        # Ушел пить чай на 10 минут (простой - idle)
        {
            "session_id": session_id,
            "timestamp": start_time + timedelta(minutes=15),
            "app": "chrome.exe",
            "window_title": "GitHub",
            "state": "idle",
            "duration": 600,
        },
        # Вернулся в VS Code на 5 минут (считаем 2-е переключение)
        {
            "session_id": session_id,
            "timestamp": start_time + timedelta(minutes=25),
            "app": "Code.exe",
            "window_title": "queries.py",
            "state": "active",
            "duration": 300,
        },
    ]

    await insert_events(events_data)

    print("4. Закрываем сессию...")
    end_time = start_time + timedelta(minutes=30)
    await end_session(session_id, ended_at=end_time)

    print("5. Запускаем расчёт аналитики...\n")
    stats = await calculate_and_save_daily_stats(user_id, target_date=start_time.date())

    print("=== ГОТОВАЯ СТАТИСТИКА ЗА ДЕНЬ ===")
    print(f"ID Пользователя: {stats['user_id']}")
    print(f"Дата: {stats['statistics_date']}")
    print(f"Фокус (сек): {stats['total_focus_time']} (ожидаем 1200 сек = 20 минут)")
    print(f"Простой (сек): {stats['total_idle_time']} (ожидаем 600 сек = 10 минут)")
    print(f"Доля простоя (idle_ratio): {stats['idle_ratio']} (ожидаем 0.3333)")
    print(f"Переключения окон: {stats['context_switches']} (ожидаем 2)")
    print(f"Топ приложений: {stats['top_apps']}")
    print("==================================\n")


if __name__ == "__main__":
    asyncio.run(main())
