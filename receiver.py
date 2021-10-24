# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 11:17:04 2021

@author: VIDUSHI
"""
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

#callback function for queue, for reading the message in the queue

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    
    
#telling which queue, which callback func
    
channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)

#loop 
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
