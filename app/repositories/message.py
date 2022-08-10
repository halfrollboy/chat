from tkinter import E
from types import coroutine
from typing import List
from os import environ
from uuid import UUID

from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from models.postgres.pg_models import Message
import models.pydantic.message as schema
from db.postgres.dependencies import get_db
from loguru import logger


class MessageRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def find(self, id: int) -> Message:
        """Поиск компании по id"""
        query = self.db.query(Message)
        return query.filter(Message.message_id == id).first()

    def find_all_by_chat_id(self, chat_id: UUID):
        """Поиск компании по email"""
        query = self.db.query(Message)
        return query.filter(Message.chat_id == chat_id).all()

    def all(self, skip: int = 0, max: int = 100) -> List[Message]:
        """Получить все сообщения"""
        query = self.db.query(Message)
        return query.offset(skip).limit(max).all()

    def create(self, message: schema.MessageBase) -> Message:
        """Создание сообщения"""
        try:
            db_messaeg = Message(**message.dict())

            self.db.add(db_messaeg)
            self.db.commit()
            self.db.refresh(db_messaeg)
            logger.debug(f"message {db_messaeg}")
            return db_messaeg
        except Exception as e:
            logger.error(
                {
                    "error": e,
                }
            )
