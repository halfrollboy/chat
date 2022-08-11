from db.rabbitmq.rabbit import Rabbit
from db.rabbitmq.cons import Consumer
from aio_pika.abc import AbstractQueue, AbstractExchange
from typing import List
from uuid import UUID

# from prod import Produser


class BrokerRepository:
    def __init__(self):
        self.consumer = None
        # self.produser = None

    async def connect_to_broker(self):
        await Rabbit.connect()

    async def init_consumer(self):
        self.consumer = Consumer()
        print(self.consumer.conn)
        await self.consumer.channel()

    # async def init_produser(self):
    #     self.produser = Produser()
    #     await self.produser.channel()

    # async def send_message(self, text: str, queue: str):
    #     message = await self.produser.create_message(text)
    #     await self.produser.send_message_to_channel(message=message, routing_key=queue)

    async def add_queue(self, q_name: str):
        """Создаём или получаем существующую очередь"""
        # Создание очереди для консумеров
        queue_concumer = await self.consumer.add_queue(q_name)
        # q_p = await self.produser.add_queue(q_name)
        return queue_concumer

    async def bind_queue_to_exchange(
        self, queues: str | List[UUID], exchange: str | List[str]
    ):
        """Биндим пользователей к чату"""
        if type(exchange) == type(""):
            for q in queues:
                self.consumer.bind_queue_to_exchange(queue_name=q, exchange=exchange)
        else:
            for e in exchange:
                self.consumer.bind_queue_to_exchange(queue_name=q, exchange=e)

    async def wait_messaging(self) -> str:
        """Ожидание получения сообщения"""
        return self.consumer.wait_message_to_channel

    async def create_exchange(self, name: str) -> AbstractExchange:
        """Создание области для очередей"""
        return await self.consumer.create_fanout_exchage(name)


async def get_broker() -> BrokerRepository:
    """Инициализируем перевичными данными и подключаем"""
    broker = BrokerRepository()
    await broker.connect_to_broker()  # Произваодим conncetion
    await broker.init_consumer()  # Создаём consumer
    # await broker.init_produser()  # Создаём producer
    return broker


# async def main() -> None:
#     c = BrokerRepository()
#     await c.connect_to_broker()
#     await c.init_consumer()
#     await c.init_produser()
#     q = await c.consumer.add_queue("online")
#     await c.send_message("user1", "online")
#     await c.consumer.wait_message_to_channel(q)


# if __name__ == "__main__":
#     asyncio.run(main())
