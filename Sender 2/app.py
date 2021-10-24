

from flask import Flask, request,jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
import pika
import sys
 

app = Flask(__name__)
app.config=['RABBIT_MQ_URL']='amqp://guest:guest@localhost:5672'
output={}


def sentiment(sentence):
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(sentence)['compound']
    if(score > 0):
        return 'This sentence is positive'
    elif(score == 0):
        return 'This sentence is neutral'
    else:
        return 'This sentence is negative'


@app.route('/', methods=['GET','POST'])
def sentimentRequest():
        if request.method=='POST':
            sentence=request.form['q']
        else:
            sentence=request.args.get('q')
        sent=sentiment(sentence)
        output['sentiment']=sent
        return jsonify(output)


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
    
    
