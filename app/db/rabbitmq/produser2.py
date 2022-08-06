import pika, time

username = "user"
password = "password"
url = f"amqp://{username}:{password}@localhost:5672/%2F?connection_attempts=3&heartbeat=3600"
# credentials = pika.PlainCredentials("user", "password")
# conn_params = pika.ConnectionParameters("localhost", 5672, credentials=credentials)
connection = pika.SelectConnection(pika.URLParameters(url))
# connection = pika.BlockingConnection(conn_params)
channel = connection.channel()
channel.queue_declare(queue="test")

channel = connection.channel()

channel.queue_declare(queue="first-queue")

for i in range(100):
    channel.basic_publish(exchange="", routing_key="first-queue", body="Hi consumer")
    print("Send")
    time.sleep(2)

connection.close()
