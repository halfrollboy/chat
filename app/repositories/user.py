from typing import List
from os import environ
from fastapi import HTTPException
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.models.pydantic.user import UserCreate

from ..models.postgres.pg_models import User
from ..db.postgres.dependencies import get_db

from passlib.context import CryptContext
from loguru import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db  # внедрение зависимостей

    def find(self, id: int) -> User:
        """Поиск пользователя по id"""
        query = self.db.query(User)
        return query.filter(User.id == id).first()

    def find_by_email(self, email: EmailStr):
        """Поиск ползователя по email"""
        query = self.db.query(User)
        return query.filter(User.email == email).first()

    def all(self, skip: int = 0, max: int = 100) -> List[User]:
        """Получить всех пользователей"""
        query = self.db.query(User)
        return query.offset(skip).limit(max).all()

    def create(self, user: UserCreate) -> User:
        """Создание пользователя"""
        faked_pass_hash = user.password + f"{ environ.get('APP_TOKEN') }"
        # faked_pass_hash = pwd_context.hash(faked_pass_hash)

        try:
            db_user = User(
                username=user.username,
                fullname=user.full_name,
                password=faked_pass_hash,
                email=user.email,
                phone=user.phone,
                # disabled=user.disabled,
            )

            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            logger.debug(f"repisytory__ db_user: {db_user}")
        except Exception as e:

            logger.debug(f"errr-{e}")
            {"error": user}
        logger.debug("success")
        # logger.debug(f"Create user {db_user.username}, email: {db_user.email}, pass: {db_user.password}")
        return db_user


# def create(self, speedster: SpeedsterCreate) -> Speedster:
#     speedster.password += "__you_must_hash_me"

#     db_speedster = Speedster(**speedster.dict())

#     self.db.add(db_speedster)
#     self.db.commit()
#     self.db.refresh(db_speedster)

#     return db_speedster
