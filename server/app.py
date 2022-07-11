from flask import Flask
import pika

app=Flask(__name__)

@app.route("/")
def hello():
    return "successfully working flask"

@app.route("/rabbit/<message>")
def rabbit_fun(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    except pika.exceptions.AMQPConnectionError as exc:
        print("Failed to connect to RabbitMQ service. Message wont be sent.")
        
    channel = connection.channel()
    channel.queue_declare(queue="test", durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='test',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2 # make msg persistent
        )
    )
    connection.close()
    return "success fully sent message"

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')

