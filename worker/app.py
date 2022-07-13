# from flask import Flask
import pika
import time

class MetaClass(type):
    _instance = {}
    
    def __call__(cls, *args, **kwargs):
        """ Singleton class called """
        if cls not in cls._instance:
            cls._instance[cls] = super(MetaClass, cls).__call__()
            return cls._instance[cls]
        
print("app called..")
class RabbitReceiver(metaclass=MetaClass):
    def __init__(self, queue="test", host="localhost"):
        print("init.......")
        self.host = host
        self.queue = queue
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.queue, durable=True)
        
    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        # time.sleep(body.count(b'.') )
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    def start_consume(self):        
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(queue=self.queue, on_message_callback=self.callback)
        self._channel.start_consuming()   
        
                
if __name__=="__main__":
    ser = RabbitReceiver(queue="random_test", host="localhost")
    ser.start_consume()
