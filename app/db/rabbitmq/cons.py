import asyncio
from uuid import UUID
import aio_pika
from typing import List
from aio_pika import ExchangeType
from aio_pika.abc import (
    AbstractQueue,
    AbstractRobustChannel,
    AbstractExchange,
    AbstractRobustConnection,
)
from db.rabbitmq.rabbit import Rabbit
from typing import Type

username = "user"
password = "password"


class Consumer(Rabbit):
    def __init__(self):
        self.QUEUE = []
        # self.routing_key = "users"
        self.exchange = None
        self._channel = None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Consumer, cls).__new__(cls)
        return cls.instance

    # TODO Использовалось для тестов
    # Может использоваться, если у нас будет только один Consumer
    # ------
    # async def connect(self) -> None:
    #     """
    #     Реализовал через classmethod чтобы можно было переподнимать
    #     подключение как из Consumer так и через Produser
    #     """
    #     self.conn = await aio_pika.connect_robust(
    #         f"amqp://{username}:{password}@localhost:5672/",
    #         on_open_callback=lambda x: print("Open connect rabbit", x),
    #         on_open_error_callback=lambda x: print("Error connect Rabbit", x),
    #         on_close_callback=lambda x: print("Rabbit Connection CLOSE", x),
    #     )
    #     self._channel = await self.conn.channel()
    #     return self.conn

    async def channel(self) -> Type[AbstractRobustChannel]:
        """Создаём сущность канал"""
        self._channel = await self.conn.channel()

    async def add_queue(self, q_name) -> Type[AbstractQueue]:
        """Создаём или получаем очердь"""
        return await self._channel.declare_queue(
            q_name,
            durable=True,
        )

    async def create_fanout_exchage(self, name: str) -> AbstractExchange:
        """Создание кастомных fanout Exchange"""
        exchange = await self._channel.declare_exchange(
            name,
            ExchangeType.FANOUT,
        )
        return exchange

    async def bind_queue_to_exchange(self, exchange: AbstractExchange, queue_name: str):
        queue, ok = await self._channel.get_queue(queue_name)
        if ok:
            await queue.bind(exchange)

    async def wait_message_to_channel(self, queue: Type[AbstractQueue]):
        """Ожидаем сообщения из канала"""
        # Ожидает максимум 10 сообещний
        # await self._channel.set_qos(prefetch_count=10)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process(ignore_processed=True):
                    await self.on_message(message=message)
                    yield message.decode()
                    # if queue.name in message.body.decode():
                    #     print("УРААААА", queue.name)

    async def on_message(self, message):
        """Функция подтверждения получения сообщения"""
        print(" [x] Done msg")
        await message.ack()


async def main() -> None:
    c = Consumer()
    # conn = await c.connect()
    q = await c.add_queue("online")
    await c.wait_message_to_channel(q)


if __name__ == "__main__":
    asyncio.run(main())
