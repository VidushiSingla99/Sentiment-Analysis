from flask import Flask, request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def main():
    if request.method=="POST":
        inp=request.form.get("inp")
        sid= SentimentIntensityAnalyzer()
        score = sid.polarity_scores(text=inp)
        if(score > 0):
            return 'This sentence is positive'
        elif(score == 0):
            return 'This sentence is neutral'
        else:
            return 'This sentence is negative'
        
        

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
    
