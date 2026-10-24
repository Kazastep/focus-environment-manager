from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from database.config import settings
import asyncio


engine = create_engine(
    url= settings.DATABASE_URL_psycopg,
    echo=False,
    pool_size=5,
    max_overflow=10
)

engine_asy = create_async_engine(
    url= settings.DATABASE_URL_asyncpg,
    echo=False,
    pool_size=5,
    max_overflow=10
)

async_session_factory = async_sessionmaker(
    bind=engine_asy,
    expire_on_commit=False
)

async def get_123():
    async with engine_asy.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        print(f'{res.all()=}')
