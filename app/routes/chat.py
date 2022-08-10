import asyncio
from time import sleep
import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from sse_starlette import EventSourceResponse
from services.chat.chat import Chat
from uuid import UUID

router_chat = APIRouter(
    prefix="/chats",
    tags=["chats"],
    # dependencies=[Depends(get_token_handler)],
    responses={404: {"messages": "Not found"}},
)

# Здесь придумать как должно выглядеть
async def data_generator():
    yield {"data": "Aлё"}
    await asyncio.sleep(10)


@router_chat.get("/{id}")
async def sever_evenets(id: UUID, chat: Chat = Depends()):
    chat.user_online()
    return EventSourceResponse(data_generator())
