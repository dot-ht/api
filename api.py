import re
from flask import Flask, request
from flask_restful import Resource, abort, Api
import pymongo
import requests
import os
import json
from dotenv import load_dotenv
from flask_cors import CORS

import pickle
import tflearn
import numpy
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

load_dotenv()
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

MONGO_CONNECTION = os.getenv('MONGO_CONNECTION')
API_KEY = os.getenv('API_KEY')
APOD = os.getenv('APOD')

myclient = pymongo.MongoClient(MONGO_CONNECTION)
mydb = myclient['planet_db']
planet_col = mydb['planet_collection']
bot_col = mydb['bot_collection']

nasa_api = requests.get(APOD + API_KEY)

with open("dataset.json") as file:
    data = json.load(file)
    
with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.load("model.tflearn")

def word_list(s, words):
    list = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                list[i] = 1

    return numpy.array(list)

def api_chat(inp):
    results = model.predict([word_list(inp, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    
    for purpose in data["purpose"]:
        for tg in purpose["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
                type = tg['response_type']
                suggestions = tg['relations']
                response = {
                    "msg" : "" if type == "img" else responses[0],
                    "img" : "" if type == "str" else responses[1],
                    "type" : type,
                    "suggestions" : suggestions
                }
    print(inp)
    return json.dumps(response)

class Day(Resource):
    def get(self):
        return_api_json = nasa_api.json()
        
        del return_api_json['date']
        del return_api_json['service_version']
        del return_api_json['media_type']
        del return_api_json['url']
        
        #return nasa api json
        return return_api_json

class Planets(Resource):
    def get(self):
        try:
            mongo_query = planet_col.find({},{ "_id": 0 })
            return_json = []
            for i in mongo_query:
                return_json.append(i)
        except:
            return "", 400
        
        return return_json, 200

class Chat(Resource):
    def get(self):
        try:
            mongo_query = bot_col.find_one({},{"_id": 0 })
        except:
            return "", 400 
        return mongo_query, 200  
        
    def post(self):
        try:
            chat_res = json.loads(api_chat(request.json['input']))
            return chat_res, 200
        except:
            return "", 400
        
    
api.add_resource(Day, '/day/')
api.add_resource(Planets, '/planets/')
api.add_resource(Chat, '/chat/')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
