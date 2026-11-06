""" Приемник роутеров наших сущностей. """
from fastapi import FastAPI

from routers.sessions import router as sessions_router
from routers.events import router as events_router
from routers.users import router as users_router

app = FastAPI()

app.include_router(sessions_router)
app.include_router(events_router)
app.include_router(users_router)