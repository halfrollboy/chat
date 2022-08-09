from pydantic import BaseModel, EmailStr, Field
import uuid
import datetime
from enum import Enum


class ChatType(Enum):
    GLOBAL = "gloabal"
    AVATAR = "avatar"
    PERSONAL = "personal"
    GROUP = "group"


class ChatBase(BaseModel):
    name = str
    type = ChatType
    title = str
    created_at = datetime.datetime
    discription = str
    photo_uri = str
    default_permissions = str
    owner_id = uuid.uuid4

    class Config:
        schema_extra = {
            "example": {
                "name": "Avatar chat 1",
                "type": "personal",
                "title": "Это супер новый чат для распродаж",
                "created_at": datetime.datetime.now(),
                "discription": "Чат для тестирования аватара",
                "photo_uri": "photo_uri",
                "default_permissions": "пока никаких",
                "owner_id": "c0b2e43b-e913-4381-9095-d564b343370a",
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
