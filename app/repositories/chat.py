from typing import List
import uuid

from fastapi.params import Depends
from sqlalchemy.orm import Session

from models.postgres.pg_models import Chat, ChatUser
from repositories.user import UserRepository
from models.pydantic.chat import ChatCreate, ChatBase
from db.postgres.dependencies import get_db
from loguru import logger


class ChatRepository:
    def __init__(
        self, db: Session = Depends(get_db), user_rep: UserRepository = Depends()
    ):
        self.db = db
        self.user_rep = user_rep

    def find(self, id: uuid.UUID) -> Chat:
        """Поиск чата по id"""
        query = self.db.query(Chat)
        return query.filter(Chat.id == id).first()

    def all(self, skip: int = 0, max: int = 100) -> List[Chat]:
        """Получить все чаты"""
        query = self.db.query(Chat)
        return query.offset(skip).limit(max).all()

    # TODO Пересмотреть создание чатика
    def create(self, chat: ChatBase) -> Chat:
        """Создание простого chata"""
        try:
            db_chat = Chat(type=chat.type)

            self.db.add(db_chat)
            self.db.commit()
            self.db.refresh(db_chat)
        except Exception as e:
            logger.error({"error": e, "chat_obj": db_chat, "data request": chat})
        logger.debug(f"Add Chat {db_chat}")
        return db_chat

    def find_user_chats(self, user_id: uuid.UUID):
        """Получить все чаты пользователя"""
        query = self.db.query(ChatUser)
        return query.filter(ChatUser.user_id == user_id).all()

    def add_user_to_chat(self, chat_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        # Тест проверяем есть ли в базе такой чат и такой пользователь
        # TODO Пока сделал без модели, чисто чтоб добавить
        chat = self.find(chat_id)
        user = self.user_rep.find(user_id)
        if chat and user:
            try:
                db_chat_user = ChatUser(chat_id=chat_id, user_id=user_id)
                self.db.add(db_chat_user)
                self.db.commit()
                self.db.refresh(db_chat_user)
                pass
            except Exception as e:
                # TODO переписать на перехват ошибки, которую возвращает база
                logger.error({"error": e, "ChatUser": db_chat_user})
            return db_chat_user

    def create_personal_chat(
        self, user_one: uuid.UUID, user_two: uuid.UUID, chat: Chat
    ):
        """Создание персонального чата"""
        created_chat = self.create(chat)

        try:
            db_chat_user1 = ChatUser(chat_id=created_chat.id, user_id=user_one)
            db_chat_user2 = ChatUser(chat_id=created_chat.id, user_id=user_two)

            self.db.add_all([db_chat_user1, db_chat_user2])
            self.db.commit()

        except Exception as e:
            logger.error(
                {
                    "error": e,
                    "chat_obj": created_chat,
                    "data reques": {"user1": user_one, "user2": user_two},
                }
            )
        logger.debug(f"Add ChatUser {[db_chat_user1, db_chat_user2]}")
        return created_chat

    def create_group_chat(self, chat: ChatCreate):
        """Создание группового чата"""
        created_chat = self.create(chat)
        participant_users = []
        try:
            for participant in chat.participants:
                participant_users.append(
                    ChatUser(chat_id=created_chat.id, user_id=participant)
                )
                self.db.add_all(participant_users)
                self.db.commit()
        except Exception as e:
            # TODO переписать на перехват ошибки, которую возвращает база
            logger.error({"error": e, "ChatUser": participant_users})
