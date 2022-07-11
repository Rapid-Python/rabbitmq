from multiprocessing import connection
import pika


print("connection server to deliver message...........")
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
except pika.exceptions.AMQPConnectionError as exc:
        print("Failed to connect to RabbitMQ service. Message wont be sent.")
        
channel = connection.channel()
channel.queue_declare(queue="test", durable=True)

print(' Waiting for messages...')
def callback(ch, method, properties, body):
    print(" Received msg %s" % body.decode())
    print(" Done")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='test', on_message_callback=callback)
channel.start_consuming()