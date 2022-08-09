import asyncio
import sys

from aio_pika import DeliveryMode, Message, connect, ExchangeType


async def main() -> None:
    # Perform connection
    connection = await connect(f"amqp://user:password@localhost:5672/")

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        message_body = (
            b" ".join(arg.encode() for arg in sys.argv[1:]) or b"Hello World!"
        )

        message = Message(
            message_body,
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        channel.declare_exchange(name="online", type=ExchangeType.DIRECT)
        # Sending the message
        await channel.default_exchange.publish(
            message,
            routing_key="online",
        )

        print(f" [x] Sent {message!r}")


if __name__ == "__main__":
    asyncio.run(main())
