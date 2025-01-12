import pika
import json

def send_request(request_data, response_data):
    # Update the request data with the response data
    request_data.update({'response': response_data})

    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare a queue (ensures the queue exists before sending messages)
    channel.queue_declare(queue='trip_queue', durable=True)

    # Publish the data to the queue
    channel.basic_publish(
        exchange='',  # Default exchange
        routing_key='trip_queue',  # Queue name as the routing key
        body=json.dumps(request_data),  # Serialize the data to JSON
        properties=pika.BasicProperties(
            delivery_mode=2  # Make the message persistent
        )
    )

    # Close the connection
    connection.close()

    print(f"Data pushed to RabbitMQ: {json.dumps(request_data)}")
