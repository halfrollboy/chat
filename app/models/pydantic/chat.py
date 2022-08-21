from pydantic import BaseModel, Field, validator
from uuid import UUID
import datetime

from enum import Enum
from typing import List


class ChatType(Enum):
    GLOBAL = "global"
    AVATAR = "avatar"
    PERSONAL = "personal"
    GROUP = "group"


class ChatBase(BaseModel):
    type: ChatType
    created_at: datetime.datetime

    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "type": "personal",
                "created_at": datetime.datetime.now(),
            }
        }


class Chat(ChatBase):
    id: UUID

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
    moderators: List[UUID]
    participants: List[UUID]

    @validator("participants")
    def check_participants(cls, v):
        if len(v) < 2:
            raise ValueError("The number of participants must be greater than 2")
        return v
