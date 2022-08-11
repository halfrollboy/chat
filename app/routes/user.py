from typing import List
from pydantic import parse_obj_as
from fastapi import APIRouter
from fastapi import APIRouter, Depends, HTTPException, status
from models.pydantic.user import User, UserBase
from repositories.user import UserRepository
from loguru import logger
from uuid import UUID

router_user = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_handler)],
    responses={404: {"user": "Not found"}},
)

# Получение всех пользователей
@router_user.get("/", response_model=List[User])
async def list_users(skip: int = 0, max: int = 10, users: UserRepository = Depends()):
    db_user = users.all(skip=skip, max=max)
    return parse_obj_as(List[User], db_user)


# Тестовое пространство получения пользователя
@router_user.get("/{user_id}", response_model=User)
async def get_user(user_id: UUID, users: UserRepository = Depends()):
    db_user = users.find(user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User.from_orm(db_user)
