from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse

from models import Session
from storage import sessions_db

router = APIRouter(prefix="/sessions")

@router.get("", status_code= status.HTTP_200_OK)
async def get_sessions():
    return sessions_db


@router.get("/{session_id}", status_code= status.HTTP_200_OK)
async def get_session(session_id:int):
    if session_id not in sessions_db:
        return JSONResponse({}, status_code= status.HTTP_404_NOT_FOUND)
    return sessions_db[session_id]


@router.post("", status_code= status.HTTP_201_CREATED)
async def post_session(session:Session):
    if not sessions_db:
        key = 1
    else:
        key = max(sessions_db.keys()) + 1

    session.session_id = key
    sessions_db[key] = session

    return session


@router.put("/{session_id}", status_code= status.HTTP_200_OK)
async def put_session(session_id:int, session:Session):
    if session_id not in sessions_db:
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)
    
    session.session_id = session_id
    sessions_db[session_id] = session

    return session


@router.delete("/{session_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_session(session_id:int):
    if session_id not in sessions_db:
        return JSONResponse({}, status_code= status.HTTP_404_NOT_FOUND)
    
    sessions_db.pop(session_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)