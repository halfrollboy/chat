# from typing import Optional
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from db.postgres.database import Model, engine
from routes.chat import router_chat
from routes.user import router_user

# import os
from loguru import logger

Model.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(router_user)
app.include_router(router_chat)


# Настройка мидвэира для прометеуса
app.add_middleware(CORSMiddleware, allow_origins=["*"])
logger.add("logs/logs.log", level="DEBUG", retention="10 days", rotation="00:00")


@app.get("/")
async def hello_world():
    return {"Hello": "World"}


@app.get("/ping")
async def read_root():
    return {"ping": "pong!"}


@router_user.get("/token")
async def get_token():
    return f"{get_auth()}"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
