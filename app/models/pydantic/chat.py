from pydantic import BaseModel, Field, validator
import uuid
import datetime
from enum import Enum
from typing import List


class ChatType(Enum):
    GLOBAL = "global"
    AVATAR = "avatar"
    PERSONAL = "personal"
    GROUP = "group"


class ChatBase(BaseModel):
    type = ChatType
    created_at = datetime.datetime

    class Config:
        schema_extra = {
            "example": {
                # "name": "Avatar chat 1",
                "type": "personal",
                # "title": "Это супер новый чат для распродаж",
                "created_at": datetime.datetime.now(),
                # "discription": "Чат для тестирования аватара",
                # "photo_uri": "photo_uri",
                # "default_permissions": "пока никаких",
                # "owner_id": "c0b2e43b-e913-4381-9095-d564b343370a",
            }
        }


class Chat(ChatBase):
    id: uuid.UUID

    class Config:
        orm_mode = True  # TL;DR; помогает связать модель со схемой

        schema_extra = {
            "example": {
                **ChatBase.Config.schema_extra.get("example"),
                "id": "e93e61ad-70a3-46c0-a377-8c5055f0c022",
            }
        }


class ChatCreate(BaseModel):
    chatname: str
    descriptions: str
    photo_uri: str
    moderators: List[uuid.UUID]
    participants: List[uuid.UUID]

    @validator("participants")
    def check_participants(cls, v):
        if len(v) < 2:
            raise ValueError("The number of participants must be greater than 2")
        return v
