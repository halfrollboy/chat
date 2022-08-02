from pydantic import BaseModel, EmailStr, ValidationError, validator


class UserBase(BaseModel):
    """Model for client"""

    username: str
    full_name: str | None = None
    disabled: bool | None = None

    class Config:
        schema_extra = {
            "example": {
                "username": "Barry Allen",
                "email": "barry.allen@starlabs.com",
                "full_name": "Piter Parker",
                "phone": "+79210707568",
                # "disabled": True,
            }
        }


# from loguru import logger
class UserCred(UserBase):
    email: EmailStr
    phone: str | None = None

    # @validator('phone')
    # def name_must_contain_space(cls, value, values, config, field):
    #     logger.debug(f"log {value}")
    #     if len(value)!=7:
    #         raise ValidationError('not a truth phone')
    #     return value


class UserCreate(UserCred):
    password: str

    class Config:
        schema_extra = {
            "example": {
                **UserBase.Config.schema_extra.get("example"),
                "password": "secret",
            }
        }


class User(UserCred):
    id: int

    class Config:
        orm_mode = True  # TL;DR; помогает связать модель со схемой

        schema_extra = {
            "example": {
                **UserBase.Config.schema_extra.get("example"),
                "id": "1",
            }
        }
