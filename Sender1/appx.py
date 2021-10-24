
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

      

connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel=connection.channel()

channel.queue_declare(queue='worker_queue'.durable=True)

channel.basic_publish(
	exchange='',
	routing_key='worker_queue',
	body=message,
	properties=pika.BasicProperties(
		delivery_mode=2,
	))

print("[x] Sent %r" % message)
connection.close()
        

if __name__ == "__main__":
    app.run()
    

    
       

sentimentAnalysis=RabbitMq()

   
    
if __name__ == '__main__':
    app.run()
