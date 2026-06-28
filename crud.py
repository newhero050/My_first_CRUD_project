from fastapi import FastAPI, status, Body
from pydantic import BaseModel, Field
from typing import List
from fastapi import HTTPException


class Message(BaseModel):
    id: int = None
    text: str

    model_config = {
        "json_schema_extra": {
            "examples":
                [
                    {
                        "text": "Simple message",
                    }
                ]
        }
    }


app = FastAPI()


messages_db = []


@app.get("/")
async def get_all_messages() -> List[Message]:
    return messages_db


@app.get("/message/{message_id}")
async def get_message(message_id: int) -> Message:
    try:
        return messages_db[message_id]
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found')


@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(message: Message) -> str:
    if len(messages_db) == 0:
        message.id = 0
    else:
        message.id = max([i.dict()['id'] for i in messages_db]) + 1
    messages_db.append(message)
    return f'Message created!'


@app.put("/message/{message_id}")
async def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = messages_db[message_id]
        edit_message.text = message
        return f"Message updated!"
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found')


@app.delete("/message/{message_id}")
async def delete_message(message_id: int) -> str:
    try:
        messages_db.pop(message_id)
        return f"Message ID={message_id} deleted!"
    except IndexError:
        raise HTTPException(status_code=404, detail='Message not found')


@app.delete("/")
async def kill_message_all() -> str:
    messages_db.clear()
    return "All messages deleted!"