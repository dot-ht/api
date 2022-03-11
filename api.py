from flask import Flask, request
from flask_restful import Resource, abort, Api
import pymongo
import requests
import os
import json

app = Flask(__name__)
api = Api(app)

MONGO_CONNECTION = os.getenv('MONGO_CONNECTION')
API_KEY = os.getenv('API_KEY')
APOD = os.getenv('APOD')

myclient = pymongo.MongoClient(MONGO_CONNECTION)
mydb = myclient['planet_db']
planet_col = mydb['planet_collection']

nasa_api = requests.get(APOD + API_KEY)

class Day(Resource):
    def get(self):
        return_api_json = nasa_api.json()
        
        del return_api_json['date']
        del return_api_json['service_version']
        del return_api_json['media_type']
        del return_api_json['url']
        
        #return nasa api json json
        return return_api_json

class Planets(Resource):
    def get(self):
        try:
            mongo_query = planet_col.find()
            return_json = []
            for i in mongo_query:
                return_json.append(i)
        except:
            return {'planets': None}, 400
        
        return {'planets': return_json}, 200

class Chat(Resource):
    def get(self):
        return {}

api.add_resource(Day, '/day/')
api.add_resource(Planets, '/planets/')
api.add_resource(Chat, '/chat/')