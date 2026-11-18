""" Приемник роутеров наших сущностей. """
from fastapi import FastAPI

from backend.routers.sessions import router as sessions_router
from backend.routers.events import router as events_router
from backend.routers.users import router as users_router

app = FastAPI()

app.include_router(sessions_router)
app.include_router(events_router)
app.include_router(users_router)