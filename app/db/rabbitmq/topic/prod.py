import asyncio
import aio_pika
import time
from rabbit import Rabbit
import sys

username = "user"
password = "password"


class Produser(Rabbit):
    def __init__(self):
        self.x = lambda a: Rabbit.connect()
        QUEUE = []
        # self._channel = None
        self.conn = None
        self.routing_key = "online"
        # Зарезервировал
        self.exchange = None
        self._channel = None

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

    # Пока будут создаваться только долговременные очереди
    # Так мы сможем контролировать кол-во сообщений и их удаление
    async def add_queue(self, q_name=""):
        """
        В очереди можно сохранять данные или нет
        для этого используются durable,exclusive, auto_delete
        """
        return await self._channel.declare_queue(
            q_name,
            durable=True,
            exclusive=False,
            auto_delete=False,  # Отключаем автоматическое удаление
        )

    async def delete_queue(self, q_name):
        await self._channel.queue_delete(q_name)

    async def create_message(self, text):
        message_body = (
            b" ".join(arg.encode() for arg in sys.argv[2:]) or b"Hello World!"
        )
        return aio_pika.Message(
            body=message_body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        )

    async def add_exchange(self):
        # await self._channel.declare_exchange()
        pass

    async def send_message_to_channel(self, message):
        async with self.conn:
            while True:
                print(f"Send msg")
                # Sending the message
                await self._channel.default_exchange.publish(
                    message,
                    routing_key="online",
                )

                print(f" [x] Sent {message!r}")
                time.sleep(3)


async def main():
    pr = Produser()
    c = await pr.connect()
    queue = await pr.add_queue(q_name="online")
    message = await pr.create_message("goblin_in_da_house")
    await pr.send_message_to_channel(message=message)


if __name__ == "__main__":
    asyncio.run(main())
