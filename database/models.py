""" Описание таблиц базы данных с помощью SQLAlchemy Core. """
from sqlalchemy import Table, UniqueConstraint, Column, Integer, Float, String,DateTime, Date, ForeignKey, MetaData
from sqlalchemy.dialects.postgresql import JSONB

metadata_obj = MetaData()

# Описание таблицы пользователей.  
users_table = Table(
    "users",
    metadata_obj,
    Column("user_id", Integer, primary_key=True),
    Column("user_name", String, nullable=False, unique=True),
    Column("user_email", String, nullable=False, unique=True),
    Column("password_hash", String, nullable=False)
)

# Описание таблици сессий. 
sessions_table = Table(
    "sessions",
    metadata_obj,
    Column("session_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.user_id"), nullable=False),
    Column("started_at", DateTime, nullable=False),
    Column("ended_at", DateTime)
)

# Описание таблицы событий. 
event_table = Table(
    "events",
    metadata_obj,
    Column("event_id", Integer, primary_key=True),
    Column("session_id", Integer, ForeignKey("sessions.session_id"), nullable=False),
    Column("timestamp", DateTime, nullable=False),
    Column("app", String, nullable=False) # nullable=False временно, возможно уберем
)

# Описание таблицы статистики
statistics_table = Table(
    "statistics",
    metadata_obj,
    Column("statistics_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.user_id"), nullable=False),
    Column("statistics_date", Date, nullable=False),
    Column("total_focus_time", Integer, nullable=False),
    Column("idle_ratio", Float),
    Column("top_apps", JSONB, nullable=False),
    Column("session_count", Integer, nullable=False),
    UniqueConstraint("user_id", "statistics_date")
)