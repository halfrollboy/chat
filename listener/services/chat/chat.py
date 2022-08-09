# По хорошему здесь вести подключения к online пользователям
from fastapi.params import Depends
from ...db.rabbitmq.broker import get_broker, BrokerRepository
from repositories.user import UserRepository
from models.postgres.pg_models import User


class Chat:
    """
    В этом классе осуществляем основную работу
    со всей логикой которая относится к чату
    Поскольку это сервис, здесь должны быть
    удобно читаемый код
    """

    async def __init__(
        self,
        broker: BrokerRepository = Depends(get_broker),
        users: UserRepository = Depends(UserRepository),
    ):
        self.broker = broker
        self.users = users

    # Попробовать с лупом запустить
    async def user_online(self, user_id):
        # Меняем статус пользователя
        self.users.edit(user_id, "is_online", True)
        # Пишем в канал оналай что появился новый пользователь
        await self.broker.send_message(
            str(user_id), "online"
        )  # # TODO Нужно ли приведение?(uuid или id) ..Отправляем сообщение в очередь
        # TODO Создаём консумера и по выходу прослушивания закрываем
        async with self.broker:
            pass
