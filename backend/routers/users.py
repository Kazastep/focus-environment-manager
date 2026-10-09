from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse

from models import User
from storage import users_db


router = APIRouter(prefix="/users")


@router.get("", status_code=status.HTTP_200_OK)
async def get_users():
    return users_db


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    if user_id not in users_db:
        return JSONResponse({},status_code=status.HTTP_404_NOT_FOUND)

    return users_db[user_id]


@router.post("", status_code=status.HTTP_201_CREATED)
async def post_user(user: User):
    if not users_db:
        key = 1
    else:
        key = max(users_db.keys()) + 1

    user.user_id = key
    users_db[key] = user

    return user


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def put_user(user_id: int, user: User):
    if user_id not in users_db:
        return JSONResponse({},status_code=status.HTTP_404_NOT_FOUND)

    user.user_id = user_id
    users_db[user_id] = user

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    if user_id not in users_db:
        return JSONResponse({},status_code=status.HTTP_404_NOT_FOUND)

    users_db.pop(user_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)