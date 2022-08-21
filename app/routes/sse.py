import asyncio
from time import sleep
import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from sse_starlette import EventSourceResponse
from services.chat.chat import Chat
from uuid import UUID

router_sse = APIRouter(
    prefix="/sse",
    tags=["sse"],
    # dependencies=[Depends(get_token_handler)],
    responses={404: {"messages": "Not found"}},
)

chat_service = Chat()

# Здесь придумать как должно выглядеть
async def data_generator(id):
    yield {"data": "Aлё"}


@router_sse.get("/{id}")
async def sever_evenets(id: UUID):
    exhange = await chat_service.user_online(id)
    return EventSourceResponse(data_generator(id))
