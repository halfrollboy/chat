# По хорошему здесь вести подключения к online пользователям
from fastapi.params import Depends
from ...db.rabbitmq.broker import BrokerRepository


async def init_broker():
    pass


class Chat:
    async def __init__(self, broker: Depends(BrokerRepository)):
        self.broker = broker
        await self.broker.connect_to_broker()
        await self.broker.init_consumer()
        await self.broker.init_produser()

    async def user_online(self, user_id):
        self.broker
