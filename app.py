from flask import Flask, request, render_template
import json
import requests
import socket
import time
from datetime import datetime
from predict import predict
import cPickle as pickle
from pymongo import MongoClient

app = Flask(__name__)
PORT = 5353
REGISTER_URL = "http://10.6.80.211:5000/register"
DATA = []
TIMESTAMP = []


@app.route('/score', methods=['POST'])
def score():
    DATA.append(request.json)
    TIMESTAMP.append(time.time())
    return ""



@app.route('/check')
def check():
    line1 = "Number of data points: {0}".format(len(DATA))
    if DATA and TIMESTAMP:
        dt = datetime.fromtimestamp(TIMESTAMP[-1])
        data_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        line2 = "Latest datapoint received at: {0}".format(data_time)
        pred = predict(DATA[-1], model, tab)
        line3 = 'Probability of fraud is {0}'.format(pred)
        ev = int(450*pred+(-50)*(1-pred))
        line4 = 'Based on cost function, expected value of classifying event as fraud is ${}'.format(ev)
        if ev > 0:
            line5 = 'Recommendation: Investigate as fraud'
        else:
            line5 = 'Recommendation: Do not investigate as fraud'

        output = "{0}\n\n{1}\n\n{2}\n\n{3}\n\n{4}".format(line1, line2, line3, line4, line5)

    else:
        output = line1

    return output, 200, {'Content-Type': 'text/css; charset=utf-8'}

def register_for_ping(ip, port):
    registration_data = {'ip': ip, 'port': port}
    requests.post(REGISTER_URL, data=registration_data)


if __name__ == '__main__':

    # Register for pinging service
    ip_address = socket.gethostbyname(socket.gethostname())
    print "attempting to register %s:%d" % (ip_address, PORT)
    register_for_ping(ip_address, str(PORT))

    # Unpickle model
    with open('model_no_dummies.pkl') as f:
        model = pickle.load(f)

    # Start Mongo
    client = MongoClient()
    db = client['fraud_db']
    tab = db['predictions']

    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)
