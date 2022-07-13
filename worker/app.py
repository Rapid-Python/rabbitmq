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
    def __init__(self, queue="random_test", host="localhost", exchange = "random-test-ex"):
        print("init.......")
        self.host = host
        self.queue = queue
        self.exchange = exchange
        
    def connection(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self._channel = self._connection.channel()
        return self._channel
    
    def  queue_declaration(self):
        try:
            self._channel.queue_declare(queue=self.queue, durable=True)
        except pika.exceptions.ChannelWrongStateError:
            self._channel = self._connection.channel()
            self._channel.queue_unbind(exchange='service.request.exchange',
                                     queue=self.queue,
                                     routing_key=self.queue)
            
            self._channel.queue_delete(self.queue)
            self._channel.queue_declare(queue=self.queue, durable=True, auto_delete=True)
        print("Queue declared....")
        print('Waiting for messages')
        
    def  exchange_declaration(self):    
        try:
            self._channel.exchange_declare(exchange='random-test-ex',
                                           exchange_type='direct')
        except pika.exceptions.ChannelClosedByBroker:
            print("$"*10, "inside exchange declare....")
            pass
        
    def  exchange_bind(self):     
        self._channel.queue_bind(exchange='random-test-ex',
                   queue=self.queue,
                   routing_key=self.queue)
  
    def callback(self, channel, method, properties, body):
        print(" [x] Received %r" % body.decode())
        time.sleep(body.count(b'.') )
        print(" [x] Done")
        self._channel.basic_ack(delivery_tag=method.delivery_tag)
        
    def start_consume(self):        
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(queue=self.queue, on_message_callback=self.callback)
        self._channel.start_consuming()   
        
                
if __name__=="__main__":
    ser = RabbitReceiver(queue="random_test", host="localhost", exchange = "random-test-ex")
    ser.connection()
    ser.queue_declaration()
    ser.exchange_declaration()
    ser.exchange_bind()
    ser.start_consume()
