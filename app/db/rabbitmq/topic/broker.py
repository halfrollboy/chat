import rabbit
from cons import Consumer
from prod import Produser


class Broker:
    rabbit.Rabbit.connect()
    consumer = Consumer()
    produser = Produser()
