import pika
import traceback, sys

username = "user"
password = "password"
url = f"amqp://{username}:{password}@localhost:5672/%2F?connection_attempts=3&heartbeat=3600"
# credentials = pika.PlainCredentials("user", "password")
# conn_params = pika.ConnectionParameters("localhost", 5672, credentials=credentials)
connection = pika.SelectConnection(pika.URLParameters(url))
# connection = pika.BlockingConnection(conn_params)
channel = connection.channel()
channel.queue_declare(queue="test")

print("waiting msg")


def callback(ch, method, properties, body):
    print(body)


try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
    traceback.print_exc(file=sys.stdout)
