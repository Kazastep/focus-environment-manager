"""
Создание таблиц PostgreSQL на основе моделей SQLAlchemy.
"""
import asyncio

from database.models import metadata_obj
from database.database import engine_asy

async def create_tables():
    async with engine_asy.begin() as conn:
        await conn.run_sync(metadata_obj.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())