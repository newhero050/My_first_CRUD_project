from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
from starlette import status

app = FastAPI()

class Post(BaseModel):
    id: int
    text: str

db =[]

async def pagination_func(limit: int = Query(10, ge=0), page: int = 1):
    return [{'limit': limit, 'page': page}]

@app.get('/messages')
async def all_messages(pagination: dict = Depends(pagination_func)):
    return {'messages': pagination}

@app.get('/comments')
async def all_comments(pagination: dict = Depends(pagination_func)):
    return {'comments': pagination}