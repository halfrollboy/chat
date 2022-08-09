import rabbit
from cons import Consumer
from prod import Produser
import asyncio


class BrokerRepository:
    def __init__(self):
        self.consumer = None
        self.produser = None

    async def connect_to_broker(self):
        await rabbit.Rabbit.connect()

    async def init_consumer(self):
        self.consumer = Consumer()
        print(self.consumer.conn)
        await self.consumer.channel()
        queue = await self.consumer.add_queue(q_name="online")

    async def init_produser(self):
        self.produser = Produser()
        await self.produser.channel()
        queue = await self.produser.add_queue(q_name="online")

    async def send_message(self, text: str, queue: str):
        message = await self.produser.create_message(text)
        await self.produser.send_message_to_channel(message=message, routing_key=queue)

    async def add_global_queue(self, q_name: str):
        # Пока сделал так,чтобы меньше мороки создания
        await self.consumer.add_queue(q_name)
        await self.produser.add_queue(q_name)
        pass


async def get_broker() -> BrokerRepository:
    """Инициализируем перевичными данными и подключаем"""
    c = BrokerRepository()
    await c.connect_to_broker()  # Произваодим conncetion
    await c.init_consumer()  # Создаём consumer
    await c.init_produser()  # Создаём producer
    q_online = await c.consumer.add_queue("online")  # Создаём очередь online
    await c.send_message("user1", "online")  # Отправляем сообщение в очередь
    q_new_message = await c.consumer.add_queue("new_message")  # Очередь новых сообщений
    await c.send_message("user1", "new_message")  # Отправляем тестовое сообщение
    await c.consumer.wait_message_to_channel(q_online)
    await c.consumer.wait_message_to_channel(q_new_message)
    return c


async def main() -> None:
    c = BrokerRepository()
    await c.connect_to_broker()
    await c.init_consumer()
    await c.init_produser()
    q = await c.consumer.add_queue("online")
    await c.send_message("user1", "online")
    await c.consumer.wait_message_to_channel(q)


if __name__ == "__main__":
    asyncio.run(main())
