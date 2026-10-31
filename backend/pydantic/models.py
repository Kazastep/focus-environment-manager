from datetime import datetime, date

from pydantic import BaseModel

""" Pydantic-модели для валидации данных. """

# Поля класса User
# Возможно разделение на UserCreate и UserRead
class User(BaseModel):
    user_id: int
    user_name: str
    user_email: str
    password_hash: str

# Поля класса Session
class Session(BaseModel):
    session_id: int | None = None
    user_id: int
    started_at: datetime
    ended_at: datetime | None = None

# Поля класса Event
class Event(BaseModel):
    event_id: int
    session_id: int
    timestamp: datetime
    app: str

# Поля класса Statistics
class Statistics(BaseModel):
    statistics_id: int
    user_id: int
    statistics_date: date
    total_focus_time: int
    idle_ratio: float
    top_apps: list[str]
    sessions_count: int