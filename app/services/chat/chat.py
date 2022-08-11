from typing import List
from fastapi.params import Depends
from db.rabbitmq.broker import get_broker, BrokerRepository

# Репозитории
from repositories.user import UserRepository
from repositories.chat import ChatRepository
from repositories.message import MessageRepository

# Модели PG
from models.postgres.pg_models import Chat as ChatModel

# Схемы данных
from models.pydantic.chat import Chat as schema_chat, ChatCreate


class Chat:
    """
    В этом классе осуществляем основную работу
    со всей логикой которая относится к чату
    Поскольку это сервис, здесь должны быть
    удобно читаемый код, как простой текст
    """

    async def __init__(
        self,
        broker: BrokerRepository = Depends(get_broker),
        users: UserRepository = Depends(),
        chat: ChatRepository = Depends(),
        message: MessageRepository = Depends(),
    ):
        self.broker = broker
        self.users = users
        self.chat = chat

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
        user_chats = [chat.id for chat in self.chat.find_user_chats(user_id)]
        for exchange in user_chats:
            await self.broker.bind_queue_to_exchange(user_id, exchange)
        # передаём не вызванную ф-цию чтобы можно было её вызвать
        # ХИТРЫЙ ТЕСТ ПЕРЕДАЧИ ТЕЛА Ф-ЦИИ НАПРЯМУЮ :)
        return self.broker.wait_messaging()

    async def create_chat(self, chat: ChatCreate):
        """Создание группового или персонального чата"""
        if len(chat.participants) == 2:
            self.chat.create_personal_chat(
                *chat.participants, schema_chat(type="personal")
            )
        self.chat.create_group_chat(chat)
        exchange = await self.broker.create_exchange(chat.chatname)
        await self.broker.bind_queue_to_exchange(chat.participants, exchange)

    # def get_all_chats(self) -> List[ChatModel]:
    #     return self.chat.all()
