# from typing import Optional
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .db.postgres.database import Model, engine
from .routes.employee import router_employee
from .routes.company import router_company
from .routes.user import router_user
from .routes.message import router_message
from .modules.auth.auth import get_auth


# import os
from loguru import logger

Model.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(router_employee)
app.include_router(router_company)
app.include_router(router_user)
app.include_router(router_message)


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
