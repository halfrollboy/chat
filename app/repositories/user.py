from typing import Any, List
from os import environ
from uuid import UUID
from fastapi.params import Depends

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models.pydantic.user as schema
from sqlalchemy import update

from models.postgres.pg_models import User
from db.postgres.dependencies import get_db
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db  # внедрение зависимостей

    async def find(self, id: UUID) -> User:
        """Поиск пользователя по id"""
        mass = await self.db.get(User, {"id": id})
        return mass

    async def all(self, skip: int = 0, max: int = 100) -> List[User]:
        """Получить всех пользователей"""
        q = await self.db.execute(select(User).order_by(User.id))
        return q.scalars().all()

    async def edit(self, user_id: UUID, atribut: str, value: Any):
        """Изменение полей данных"""
        atr = getattr(User, atribut)
        if getattr(User, atribut):
            try:
                q = update(User).where(User.id == user_id).values(atr=value)
                q.execution_options(synchronize_session="fetch")
                await self.db.execute(q)
                await self.db.commit()
            except SQLAlchemyError:
                print("err")
                await self.db.rollback()
                return {"db error": "error"}
            return True
        else:
            return {"atribut": False}

    async def create(self, user: schema.User) -> User:
        """Создание пользователя"""
        try:
            db_user = User(**user.dict())
            self.db.add(db_user)
            await self.db.commit()
            await self.db.flush()
            logger.debug(f"create User: {db_user}")
        except Exception as e:
            logger.error(f"errr-{e}", {"error": user})

        logger.debug("success")
        return db_user


# class UserReposytorySSE():
#     db =
