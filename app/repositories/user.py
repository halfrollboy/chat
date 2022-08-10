from typing import Any, List
from os import environ
from uuid import UUID
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models.pydantic.user as schema

from models.postgres.pg_models import User
from db.postgres.dependencies import get_db
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db  # внедрение зависимостей

    def find(self, id: UUID) -> User:
        """Поиск пользователя по id"""
        query = self.db.query(User)
        return query.filter(User.id == id).first()

    def all(self, skip: int = 0, max: int = 100) -> List[User]:
        """Получить всех пользователей"""
        query = self.db.query(User)
        return query.offset(skip).limit(max).all()

    def edit(self, user_id: str, atribut: str, value: Any):
        """Изменение полей данных"""
        atr = getattr(User, atribut)
        if getattr(User, atribut):
            try:
                query = (
                    self.db.query(User)
                    .filter(User.id == user_id)
                    .update({atr: value}, synchronize_session=False)
                )
                self.db.commit()
            except SQLAlchemyError:
                self.db.rollback()
                return {"error": "error"}
            return True
        else:
            return False

    def create(self, user: schema.User) -> User:
        """Создание пользователя"""

        try:
            # Переносим все поля модели pydantic в модель пользователя
            # Правда работать это будет пока не добавим пароли
            db_user = User(**user.dict())

            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            logger.debug(f"create User: {db_user}")
        except Exception as e:
            logger.error(f"errr-{e}", {"error": user})

        logger.debug("success")
        return db_user
