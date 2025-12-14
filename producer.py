import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue')

def send_message(msg):
    channel.basic_publish(exchange='', routing_key='task_queue', body=msg)
    print(f" [x] Sent {msg}")

if __name__ == '__main__':
    send_message('Hello from producer!')
    connection.close()
