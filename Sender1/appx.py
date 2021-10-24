
from flask import Flask, request, render_template,Response
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pika
import sys
import uuid

from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
stopwords=set(stopwords.words('english'))

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('form.html')

@app.route('/submit',methods=['POST','GET'])
def sentimentanaly():
    if request.method=="POST":
         message = sentimentAnalysis.call(request.form['Message'])
    return Response( message)

@app.route('/', methods=['POST'])
def my_form_0():
        
    #remove stopwords    
    docx = ' '.join([word for word in textt.split() if word not in stopwords])
    sa = SentimentIntensityAnalyzer()
    score = sa.polarity_scores(text=docx)
    compound = round((1 + score['compound'])/2, 2)

    return render_template('form.html', final=compound, text1=textt,text2=score['pos'],text5=score['neg'],text4=compound,text3=score['neu'])

class RabbitMq(object):
     def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

     def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

     def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return (self.response)
       

sentimentAnalysis=RabbitMq()

   
    
if __name__ == '__main__':
    app.run()