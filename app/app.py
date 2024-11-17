from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pika
import json

app = FastAPI()

# RabbitMQ connection parameters
RABBITMQ_HOST = "rabbitmq"

class BrowseRequest(BaseModel):
    url: str

@app.post("/browse")
def browse(request: BrowseRequest):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='browse_queue', durable=True)

    message = {"url": request.url}
    channel.basic_publish(
        exchange='',
        routing_key='browse_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()
    return {"message": "Task added to queue"}
