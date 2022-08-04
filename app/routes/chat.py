import asyncio
from time import sleep
import uvicorn
from fastapi import FastAPI, APIRouter
from sse_starlette import EventSourceResponse

router_message = APIRouter(
    prefix="/chats",
    tags=["chats"],
    # dependencies=[Depends(get_token_handler)],
    responses={404: {"messages": "Not found"}},
)

# Здесь придумать как должно выглядеть
async def data_generator():
    yield {"data": "Aлё"}
    await asyncio.sleep(10)


@app.get("/")
async def sever_evenets():
    return EventSourceResponse(data_generator())
