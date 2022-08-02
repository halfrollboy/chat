from pydantic import BaseModel, EmailStr


class CompanyBase(BaseModel):
    name: str
    phone: str
    info_id: int | None
    email: EmailStr
    adress: str | None
    coordinate: str | None

    class Config:
        schema_extra = {
            "example": {
                "name": "Flame2",
                "phone": "89210707569",
                "info_id": 2,
                "email": "stiker777@mail.com",
                "adress": "Soviet union",
                "coordinate": "какие-то координаты",
            }
        }


class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True  # TL;DR; помогает связать модель со схемой

        schema_extra = {
            "example": {
                **CompanyBase.Config.schema_extra.get("example"),
                "id": "1",
            }
        }


class EmployeeBase(BaseModel):
    name: str
    phone: str
    email: EmailStr
    company_id: int
    gender: bool
    owner: int | None
    admin: int | None

    class Config:
        schema_extra = {
            "example": {
                "name": "Barry Allen",
                "phone": "+79210707568",
                "email": "barry.allen@starlabs.dc",
                "company_id": 1,
                "gender": True,
                "owner": True,
                "admin": False,
            }
        }


# Пароль никогда не должен быть возвращен в ответе.
# Для этого используется третья схема, определенная ниже.
# Проверяется только запрос на создание.
class EmployeeCreate(EmployeeBase):
    password: str

    class Config:
        schema_extra = {
            "example": {
                **EmployeeBase.Config.schema_extra.get("example"),
                "password": "secret",
            }
        }


class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True  # TL;DR; помогает связать модель со схемой

        schema_extra = {
            "example": {
                **EmployeeBase.Config.schema_extra.get("example"),
                "id": "1",
            }
        }
