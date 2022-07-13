from flask import Flask
import pika
from random import randint

app=Flask(__name__)
class MetaClass(type):
    _instance = {}
    
    def __call__(cls, *args, **kwargs):
        """ Singleton class called """
        if cls not in cls._instance:
            print("inside")
            cls._instance[cls] = super(MetaClass, cls).__call__()
        return cls._instance[cls]
       
        
class RabbitConfig(metaclass=MetaClass):
    def __init__(self, exchange="", host="localhost", queue="test", routing_key="test"):
        self.exchange = exchange
        self.host = host
        self.queue = queue
        self.routing_key = routing_key

class RabbitService():
    def __init__(self, config):
        self.config = config
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config.host)
            )
        self._channel = self._connection.channel()
        self._channel.queue_declare(self.config.queue, durable=True)
          
    def rabbit_message(self, payload={}):
        print("Publishing message.....")
        self._channel.basic_publish(
                                exchange=self.config.exchange,
                                routing_key=self.config.routing_key,
                                body=str(payload),
                                properties=pika.BasicProperties(
                                    delivery_mode=2 # make msg persistent
                                )
                            )
        print("Published message.....")
        
    def exit(self):
        self._connection.close()
        
@app.route("/app")
def called_fun():
    config = RabbitConfig(exchange="", host="localhost", queue="random_test", routing_key="")
    server = RabbitService(config)
    for i in range(0,20000):
        server.rabbit_message({"data":f"Index No.{i}: {randint(0,10000)} "})
        print("Published message.....")
    return "Published message....."
    

if __name__=="__main__":
    
    app.run(debug=True, host='0.0.0.0')

