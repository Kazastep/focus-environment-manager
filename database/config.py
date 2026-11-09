""" Загрузка настроек PostgreSQL и формирование URL подключения."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from sqlalchemy.engine import URL

# Определяем путь к файлу с переменными окружения.
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    POSTGRES_HOST: str

    # Синхронное подключение для теста
    # @property
    # def DATABASE_URL_psycopg(self):
    #     return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Асинхронное подключение с sqlalchemy URL
    @property
    def DATABASE_URL_asyncpg(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )

    # Указываем источник настроек — файл .env.
    model_config = SettingsConfigDict(env_file=ENV_FILE)

# Создаём объект настроек для использования в проекте.
settings = Settings()