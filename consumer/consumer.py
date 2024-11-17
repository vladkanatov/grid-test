import pika
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# RabbitMQ connection parameters
RABBITMQ_HOST = "rabbitmq"

def wait_for_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            connection.close()
            print("RabbitMQ is ready")
            break
        except pika.exceptions.AMQPConnectionError:
            print("Waiting for RabbitMQ...")
            time.sleep(2)

def process_message(ch, method, properties, body):
    message = json.loads(body)
    url = message["url"]

    
    options = Options()
    options.add_argument('--headless')  # Если нужен headless режим
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Remote(
        command_executor='http://selenium-hub:4444/wd/hub',
        options=options
    )

    try:
        driver.get(url)
        print(f"HTML content of {url}:")
        print(driver.page_source)
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
    finally:
        driver.quit()

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    wait_for_rabbitmq()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue='browse_queue', durable=True)

    # Start consuming
    channel.basic_consume(queue='browse_queue', on_message_callback=process_message)
    print("Waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
