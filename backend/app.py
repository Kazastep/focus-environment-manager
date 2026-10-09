from fastapi import FastAPI, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

_db = {}

class Item(BaseModel):
    id: None | int = None
    name: str = 'Name'
    

@app.get("/items/{item_id}")
async def get_item(item_id:int):
    if item_id not in _db.keys():
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)
    return _db[item_id]


@app.post("/items", status_code=status.HTTP_201_CREATED)
async def post_item(item:Item):
    if not _db:
        key = 1
    else:
        key = max(_db.keys()) + 1
    item.id = key
    _db[key] = item
    return item


@app.delete("/items/{item_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id:int):
    if item_id not in _db.keys():
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)
    _db.pop(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/items/{item_id}")
async def put_item(item_id:int, item:Item):
    if item_id not in _db.keys():
        return JSONResponse({}, status_code=status.HTTP_404_NOT_FOUND)
    item.id = item_id
    _db[item_id] = item
    return item
    