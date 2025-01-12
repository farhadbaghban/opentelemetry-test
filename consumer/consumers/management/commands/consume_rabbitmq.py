from django.core.management.base import BaseCommand
import pika  # RabbitMQ client
import json
from consumers.models import RequestResponse  # Update with your Django app name

class Command(BaseCommand):
    help = 'Consume messages from RabbitMQ and save to the database'

    def handle(self, *args, **kwargs):
        # Establish a connection to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # Declare the queue we will consume from
        channel.queue_declare(queue='trip_queue', durable=True)

        # Callback function to process messages
        def callback(ch, method, properties, body):
            try:
                # Deserialize the incoming message
                data = json.loads(body)

                # Extract data from the message
                req_method = data.get('method')
                url = data.get('url')
                request = data.get('body', {})  # Provide default empty dict if 'body' is missing
                headers = data.get('headers', {})
                response = data.get('response')

                if not req_method or not url:
                    print("Invalid message format: Missing required fields.")
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    return

                # Check if request is None or empty, set it to an empty dict if it is
                if request is None:
                    request = {}

                # Save the data to the database
                obj = RequestResponse.objects.create(
                    method=req_method,
                    url=url,
                    request=request,
                    response=response,
                    headers=headers
                )

                print(f" [x] Processed and saved: {obj}")

                # Acknowledge that the message has been processed successfully
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                print(f"Error processing message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag)

        # Start consuming messages
        channel.basic_consume(queue='trip_queue', on_message_callback=callback)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
