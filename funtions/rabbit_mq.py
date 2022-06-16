# import json
#
# import pika
#
# connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
# channel = connection.channel()
#
#
# def publish_base(method, body):
#     properties = pika.BasicProperties(method)
#     channel.basic_publish(
#         exchange='',
#         routing_key='example_rabbitMQ',
#         body=json.dumps(body),
#         properties=properties)
