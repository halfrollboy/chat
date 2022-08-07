import asyncio
import aio_pika

from rabbit import Rabbit

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

    async def connect(self) -> None:
        """
        Реализовал через classmethod чтобы можно было переподнимать
        подключение как из Consumer так и через Produser
        """
        print("Get conn")  # TODO переписать print на логи и сделать settings
        self.conn = await aio_pika.connect_robust(
            f"amqp://{username}:{password}@localhost:5672/",
            on_open_callback=lambda x: print("Open connect rabbit", x),
            on_open_error_callback=lambda x: print("Error connect Rabbit", x),
            on_close_callback=lambda x: print("Rabbit Connection CLOSE", x),
        )
        self._channel = await self.conn.channel()
        return self.conn

    async def channel(self):
        self._channel = await self.conn.channel()

    async def add_queue(self, q_name):
        # Declaring queue
        return await self._channel.declare_queue(
            q_name,
            durable=True,
        )

    async def wait_message_to_channel(self, queue):
        print("wait now")
        async with self.conn:
            # Отправляет максимум 10 сообещний
            # await self._channel.set_qos(prefetch_count=10)
            print("wel")
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    self.on_message(message=message)
                    print("mes")
                    async with message.process():
                        print("MESSAGE BODY", message.body)

                        if queue.name in message.body.decode():
                            print("УРААААА", queue.name)

    async def on_message(self, message):
        await asyncio.sleep(message.body.count(b"."))
        print(" [x] Done msg")
        await message.ack()


async def main() -> None:
    c = Consumer()
    # conn = await c.connect()
    q = await c.add_queue("online")
    await c.wait_message_to_channel(q)


if __name__ == "__main__":
    asyncio.run(main())
