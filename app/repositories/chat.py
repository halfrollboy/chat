from typing import List
import uuid

from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from ..models.postgres.pg_models import Chats
from ..db.postgres.dependencies import get_db
from loguru import logger


class ChatRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def find(self, id: uuid.UUID) -> Chats:
        """Поиск компании по id"""
        query = self.db.query(Chats)
        return query.filter(Chats.id == id).first()

    def find_by_email(self, name: EmailStr):
        """Поиск чатов по email"""
        query = self.db.query(Chats)
        return query.filter(Chats.name == name).first()

    def all(self, skip: int = 0, max: int = 100) -> List[Chats]:
        """Получить все чаты"""
        query = self.db.query(Chats)
        return query.offset(skip).limit(max).all()

    # TODO Пересмотреть создание чатика
    def create(self, chat: Chats) -> Chats:
        """Создание chata"""

        db_chat = Chats(
            name=chat.name,
            type=chat.type,
            title=chat.title,
            created_at=chat.created_at,
            discription=chat.discription,
            photo_uri=chat.photo_uri,
            default_permissions=chat.default_permissions,
            owner_id=chat.owner_id,
        )

        self.db.add(db_chat)
        self.db.commit()
        self.db.refresh(db_chat)
        logger.debug(f"Chat {db_chat}")
        return db_chat
