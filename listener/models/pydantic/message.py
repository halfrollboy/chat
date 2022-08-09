from pydantic import BaseModel, EmailStr, Field
from uuid import uuid4, UUID
import datetime
from typing import List
from enum import Enum


class MessageType(Enum):
    GLOBAL = "gloabal"
    AVATAR = "avatar"
    PERSONAL = "personal"
    GROUP = "group"


class MessageBase(BaseModel):
    "Базовая модель сообщений"
    chat_id = UUID
    user_id = UUID
    reply_to = int
    created_at = datetime.datetime
    edited_at = datetime.datetime
    content = str
    attachment = List[UUID]

    class Config:
        schema_extra = {
            "example": {
                "chat_id": "e93e61ad-70a3-46c0-a377-8c5055f0c022",
                "user_id": "",
                "type": "personal",
                "title": "Это супер новый чат для распродаж",
                "created_at": datetime.datetime.now(),
                "discription": "Чат для тестирования аватара",
                "photo_uri": "photo_uri",
                "default_permissions": "пока никаких",
                "owner_id": "c0b2e43b-e913-4381-9095-d564b343370a",
            }
        }


class Message(MessageBase):
    id: int

    class Config:
        orm_mode = True  # TL;DR; помогает связать модель со схемой

        schema_extra = {
            "example": {
                **MessageBase.Config.schema_extra.get("example"),
                "id": "1",
            }
        }
