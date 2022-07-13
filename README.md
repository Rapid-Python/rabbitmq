# rabbitmq with docker

## What Is RabbitMQ
    RabbitMQ is a fairly popular asynchronous message broker that can handle millions of messages.It originally implemented the Advanced Message Queuing Protocol (AMQP) but has been extended to support Streaming Text Oriented Messaging Protocol (STOMP), Message Queuing Telemetry Transport (MQTT), and other protocols.

    you should be able to connect to http://locahost:15672 and see the RabbitMQ management console. Use the username and password guest to login

## What is docker
    Docker helps developers build lightweight and portable software containers that simplify application development, testing, and deployment

    Install Docker using official documentation 
    https://docs.docker.com/engine/install/

## To run docker

```bash
$ docker-compose up -d

```

## To run worker
```bash
$ python3 worker/app.py

```

## To run server
```bash
$ python3 server/app.py

```

## To publish message from server
```bash
$  localhost:8000/app/

```