from datetime import datetime
from re import U
from typing import List
import uuid

from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from models.postgres.pg_models import Chat, ChatUser, GroupChat, Message, ChatType
from repositories.user import UserRepository
from models.pydantic.chat import ChatCreate, ChatBase, Chat as ChatScheme
from db.postgres.dependencies import get_db
from loguru import logger
from sqlalchemy import select, update, delete
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError


class ChatRepository:
    def __init__(
        self, db: AsyncSession = Depends(get_db), user_rep: UserRepository = Depends()
    ):
        self.db = db
        self.user_rep = user_rep

    async def find(self, chat_id: uuid.UUID) -> Chat:
        """Поиск чата по id"""
        q = await self.db.get(Chat, {"id": chat_id})
        return q.scalars().first()

    async def all(self, skip: int = 0, max: int = 100) -> List[Chat]:
        """Получить все чаты"""
        q = await self.db.execute(select(Chat))
        return q.scalars().all()

    async def create(self, type: ChatType) -> Chat:
        """Создание простого chata"""
        try:
            db_chat = Chat(type=type)

            await self.db.add(db_chat)
            await self.db.commit()
            await self.db.refresh(db_chat)
            logger.debug(f"Add Chat {db_chat}")
        except Exception as e:
            logger.error({"error": e, "data request": db_chat})
        return db_chat

    async def find_user_chats(self, user_id: uuid.UUID) -> List[Chat]:
        """Получить все чаты пользователя"""
        list_chat = await self.db.get(Chat, {"user_id": id})
        return list_chat

    async def add_user_to_chat(self, chat_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        # Тест проверяем есть ли в базе такой чат и такой пользователь
        # TODO Пока сделал без модели, чисто чтоб добавить
        chat = await self.find(chat_id)
        user = await self.user_rep.find(user_id)
        if chat and user:
            try:
                db_chat_user = ChatUser(chat_id=chat_id, user_id=user_id)
                await self.db.add(db_chat_user)
                await self.db.commit()
                self.db.refresh(db_chat_user)

            except Exception as e:
                # TODO переписать на перехват ошибки, которую возвращает база
                logger.error({"error": e, "ChatUser": db_chat_user})

            return db_chat_user

    async def create_personal_chat(
        self, user_one: uuid.UUID, user_two: uuid.UUID, chat: Chat
    ):
        """Создание персонального чата"""
        created_chat = await self.create("personal")

        try:
            chat = Chat(type="personal")
            db_chat_user1 = ChatUser(chat_id=created_chat.id, user_id=user_one)
            db_chat_user2 = ChatUser(chat_id=created_chat.id, user_id=user_two)

            await self.db.add_all([chat, db_chat_user1, db_chat_user2])
            await self.db.commit()

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

    async def create_group_chat(self, chat: ChatCreate):
        """Создание группового чата"""
        # Нам требуется получить id чата поэтому сначала создаём его в базе
        created_chat = await self.create("group")
        participant_users = []
        try:
            for participant in chat.participants:
                participant_users.append(
                    GroupChat(chat_id=created_chat.id, **chat),
                    ChatUser(chat_id=created_chat.id, user_id=participant),
                )
                await self.db.add_all(participant_users)
                await self.db.commit()
        except Exception as e:
            # TODO переписать на перехват ошибки, которую возвращает база
            logger.error({"error": e, "ChatUser": participant_users})

    async def find_group_info(self, chat_id: uuid.UUID):
        """Поиск информации групповых чатов"""
        q = await self.db.execute(select(GroupChat).where(GroupChat.id == chat_id))
        return q.fetchall()

    async def find_chat_name(self, name):
        """Найти имя чата"""
        q = await self.db.execute(select(GroupChat).where(GroupChat.name == name))
        return q.fetchall()

    async def mute_chat(
        self,
        user_id: uuid.UUID,
        chat_id: uuid.UUID,
        time: datetime = None,
    ):
        """Мутим сообщения из чата"""
        if time == None:
            time = "null"

        try:
            # Были проблемы с запросом через alchemy
            query_str = """
                UPDATE chat_user
                SET is_muted = NOT is_muted, 
                WHERE chat_id = '{}' and user_id = '{}'
                RETURNING *;
            """.format(
                chat_id, user_id
            )

            await self.db.execute(query_str)
            await self.db.commit()

        except SQLAlchemyError:
            print("err")
            await self.db.rollback()
            return {"db error": "error"}
        return True

    async def leave_from_chat(self, chat_id: uuid.UUID, user_id: uuid.UUID):
        """Выход из чата
        С возможностью вернуться
        """
        try:
            stmt = select(Message).where(
                Message.created_at
                == select(func.max(Message.created_at)).where(
                    Message.chat_id == chat_id
                ),
            )

            result = await self.db.execute(stmt)
            instance = result.scalars().first()

            q = (
                update(ChatUser)
                .where(ChatUser.user_id == user_id, ChatUser.chat_id == chat_id)
                .values(is_left=True, last_read_id=instance.message_id)
            )
            q.execution_options(synchronize_session="fetch")
            await self.db.execute(q)
            await self.db.commit()
            return "ok"
        except Exception as e:
            logger.error({"error": e, "chat-user": chat_id})
        return "false"

    async def delete_user_from_chat(self, user_id: uuid.UUID, chat_id: uuid.UUID):
        """Удаление пользователя из чата
        Без варианта вернуться
        Только по новому приглашению
        """
        try:
            q = delete(ChatUser).where(
                ChatUser.user_id == user_id, ChatUser.chat_id == chat_id
            )
            q.execution_options(synchronize_session="fetch")
            await self.db.execute(q)
            await self.db.commit()
            return "ok"
        except Exception as e:
            logger.error({"error": e, "chat-user": chat_id})
        return "false"

    async def last_read_message(
        self, chat_id: uuid.UUID, message_id: uuid.UUID, user_id: uuid.UUID
    ):
        try:
            q = (
                update(ChatUser)
                .where(ChatUser.chat_id == chat_id, ChatUser.user_id == user_id)
                .values(last_read_id=message_id)
            )
            q.execution_options(synchronize_session="fetch")
            await self.db.execute(q)
            await self.db.commit()
        except SQLAlchemyError:
            print("err")
            await self.db.rollback()
            return {"db error": "error"}
        return True


# 3dfd56a1-c613-4d2a-a538-9d1a0d9a200b
# 14
