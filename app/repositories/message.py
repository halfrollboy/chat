from tkinter import E
from types import coroutine
from typing import List
from os import environ
from uuid import UUID

from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from uuid import UUID
from models.postgres.pg_models import Message, Attachment
import models.pydantic.message as schema
from db.postgres.dependencies import get_db
from loguru import logger

from sqlalchemy import select, update, delete


class MessageRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def find(self, id: UUID) -> Message:
        """Поиск компании по id"""
        message = await self.db.get(Message, {"id": id})
        return message

    async def get_message_with_chat(self, message_id: int, chat_id: UUID):
        message = await self.db.get(
            Message, {"message_id": message_id, "chat_id": chat_id}
        )
        return message

    async def get_messages_by_chat_id(self, chat_id: UUID) -> List[Message]:
        """Получить все сообщения из чата"""
        q = await self.db.execute(select(Message).where(Message.chat_id == chat_id))
        return q.fetchall()

    async def all(self, skip: int = 0, max: int = 100) -> List[Message]:
        """Получить все сообщения"""
        q = await self.db.execute(select(Message))
        return q.scalars().all()

    async def create(self, message: schema.MessageBase) -> Message:
        """Создание сообщения"""
        try:
            db_messaeg = Message(**message.dict())

            await self.db.add(db_messaeg)
            await self.db.commit()
            await self.db.refresh(db_messaeg)
            logger.debug(f"message {db_messaeg}")
            return db_messaeg
        except Exception as e:
            logger.error(
                {
                    "create error": e,
                }
            )

    async def delete_message_from_chat(self, chat_id: UUID, message_id: int):
        """Удаление сообщения из чата"""
        try:
            q = delete(Message).where(
                Message.message_id == message_id, Message.chat_id == chat_id
            )
            q.execution_options(synchronize_session="fetch")
            await self.db.execute(q)
            await self.db.commit()
            return "ok"
        except Exception as e:
            logger.error({"error": e, "chat-user": chat_id})
        return "false"

    async def get_attachemnts_unic(self, chat_id: UUID) -> Attachment:
        """Получени уникальных attachments из чата"""
        sql = """with reco as (
            SELECT distinct unnest(attachments) item_attach
            FROM messages item
            where chat_id = '{}'
            )
            select * from reco
            join attachments att on att.attachment_id = item_attach""".format(chat_id)
        query = await self.db.execute(sql)
        return query.fetchall()
