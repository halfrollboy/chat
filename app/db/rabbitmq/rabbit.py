import asyncio

import aio_pika
import time

from db.rabbitmq.config import get_db_settings

username = "user"
password = "password"

settings = get_db_settings()


class Rabbit:
    conn = None

    @classmethod
    async def connect(cls) -> None:
        """
        Реализовал через classmethod чтобы можно было переподнимать
        подключение как из Consumer так и через Produser
        """
        print("Get conn")  # TODO переписать print на логи и сделать settings
        cls.conn = await aio_pika.connect_robust(
            # "amqp://guest:guest@127.0.0.1/",
            f"amqp://{username}:{password}@localhost:5672/",
            on_open_callback=lambda x: print("Open connect rabbit", x),
            on_open_error_callback=lambda x: print("Error connect Rabbit", x),
            on_close_callback=lambda x: print("Rabbit Connection CLOSE", x),
        )
