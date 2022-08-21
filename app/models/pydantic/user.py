from dataclasses import Field
from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel
from enum import Enum


class GenderType(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    middlename: str | None
    gender: GenderType
    birthday: date
    photo_uri: str

    class Config:
        schema_extra = {
            "example": {
                "username": "boogeyman",
                "firstname": "Piter",
                "lastname": "Parker",
                "middlename": "Petrovich",
                "gender": "male",
                "birthday": "2022-08-10 15:45:43.842195",
                "photo_uri": "00000000",
            }
        }


class User(UserBase):
    id: UUID

    class Config:
        orm_mode = True  # TL;DR; помогает связать модель со схемой

        schema_extra = {
            "example": {
                **UserBase.Config.schema_extra.get("example"),
                "id": "5dc763fe-579f-4436-aa25-5ee5681e839e",
            }
        }
