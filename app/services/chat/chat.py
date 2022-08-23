from email import message
from typing import List
from fastapi.params import Depends
from db.rabbitmq.broker import get_broker, BrokerRepository
from uuid import UUID

# Репозитории
from repositories.user import UserRepository
from repositories.chat import ChatRepository
from repositories.message import MessageRepository

# Модели PG
from models.postgres.pg_models import Chat as ChatModel, Message

# Схемы данных
from models.pydantic.chat import Chat as schema_chat, ChatCreate


class Chat:
    """
    В этом классе осуществляем основную работу
    со всей логикой которая относится к чату
    Поскольку это сервис, здесь должны быть
    удобно читаемый код, как простой текст
    """

    def __init__(self, broker: BrokerRepository = Depends(get_broker)):
        self.broker = broker
        self.users = UserRepository()
        self.chat = ChatRepository()
        self.message = MessageRepository()

    async def user_online(self, user_id):
        """
        1 - Меняем статус в базе { Deprecated }
        2 - Создаём очередь с name = user_id
        3 - Получаем все чаты пользователя
        4 - Добавляем очередь во все excahge чатов
        """
        # TODO { Deprecated } Меняем статус пользователя
        self.users.edit(user_id, "is_online", True)
        q = self.broker.add_queue(str(user_id))
        user_chats = [chat.chat_id for chat in self.chat.find_user_chats(user_id)]
        for exchange in user_chats:
            await self.broker.bind_queue_to_exchange(user_id, exchange)
        # передаём не вызванную ф-цию чтобы можно было её вызвать
        return self.broker.wait_messaging()

    async def create_chat(self, chat: ChatCreate):
        """Создание группового или персонального чата"""
        if len(chat.participants) == 2:
            self.chat.create_personal_chat(
                *chat.participants, schema_chat(type="personal")
            )
        resp = await self.chat.create_group_chat(chat)
        print(self.broker)
        print(chat.chatname)
        exchange = await self.broker.create_exchange(chat.chatname)
        await self.broker.bind_queue_to_exchange(chat.participants, exchange)
        return "ok"

    async def check_name_is_free(self, name: str) -> bool:
        """
        Проверка на доступность имени
        Поиск только по групповым чатам
        """
        mass = await self.chat.find_chat_name(name)
        if len(mass) > 0:
            return False
        return True

    async def mute_chat(self, user_id: UUID, chat_id: UUID):
        """Мьютим чат для пользователя"""
        await self.chat.mute_chat(user_id=user_id, chat_id=chat_id)

    async def get_messages_from_chat(self, chat_id: UUID) -> List[Message]:
        """Получаем все сообщения из чата"""
        await self.message.get_messages_by_chat_id(chat_id=chat_id)

    # def get_all_chats(self) -s> List[ChatModel]:
    #     return self.chat.all()

    # async def delete_user_from_chat(self, chat_id: UUID, message_id: UUID) -> Message:

    # await self.message.find()

    async def add_user_to_chat(self):
        """Приглашение пользователя по инвайту"""
        #
        pass
