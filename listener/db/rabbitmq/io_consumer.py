import asyncio

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage


async def on_message(message: AbstractIncomingMessage) -> None:
    async with message.process():
        print(f" [x] Received message {message!r}")
        print(f"     Message body is: {message.body!r}")


async def main() -> None:
    # Perform connection
    connection = await connect(f"amqp://user:password@localhost:5672/")

    async with connection:
        # Creating a channel
        channel = await connection.channel()
        # await channel.set_qos(prefetch_count=1)

        # Declaring queue
        queue1 = await channel.declare_queue(
            "online",
            durable=True,
        )
        queue2 = await channel.declare_queue(
            "online2",
            durable=True,
        )

        # Start listening the queue with name 'task_queue'
        await queue1.consume(on_message)
        await queue2.consume(on_message)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
