"""
Создание таблиц PostgreSQL на основе моделей SQLAlchemy.
"""
import asyncio

from database.models import metadata_obj
from database.database import engine_asy

async def create_tables():
    """Создаёт отсутствующие таблицы, зарегистрированные в metadata_obj."""
    
    # Открываем соединение с БД и начинаем транзакцию.
    async with engine_asy.begin() as conn:
        # create_all — синхронный метод, поэтому используем run_sync.
        await conn.run_sync(metadata_obj.create_all)

# Выполнение функции только при прямом запуске файла.
if __name__ == "__main__":
    asyncio.run(create_tables())