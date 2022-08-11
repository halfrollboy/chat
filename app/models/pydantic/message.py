from pydantic import BaseModel
from uuid import uuid4, UUID
import datetime
from typing import List
from enum import Enum

from models.postgres.pg_models import Attachment


class MessageType(Enum):
    GLOBAL = "gloabal"
    AVATAR = "avatar"
    PERSONAL = "personal"
    GROUP = "group"


class MessageBase(BaseModel):
    chat_id: UUID
    user_id: UUID
    reply_to: int | None
    content: str
    attachment: List[UUID] | None

    class Config:
        schema_extra = {
            "example": {
                "chat_id": "e93e61ad-70a3-46c0-a377-8c5055f0c022",
                "user_id": "5dc763fe-579f-4436-aa25-5ee5681e839e",
                "type": "personal",
                "reply_to": None,
                "content": str,
                "attachment": None,
            }
        }


class EditedMessage(MessageBase):
    edited_at = datetime.datetime
    schema_extra = {
        "example": {
            **MessageBase.Config.schema_extra.get("example"),
            "edited_at": "2022-08-10 16:17:05.174747",
        }
    }


class Message(MessageBase):
    message_id: int

    class Config:
        orm_mode = True  # TL;DR; помогает связать модель со схемой

        schema_extra = {
            "example": {
                **MessageBase.Config.schema_extra.get("example"),
                "id": "1",
            }
        }
