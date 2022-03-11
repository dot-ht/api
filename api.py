from flask import Flask, request
from flask_restful import Resource, abort, Api
import pymongo
import os
import json

app = Flask(__name__)
api = Api(app)

MONGO_CONNECTION = os.getenv('MONGO_CONNECTION')

myclient = pymongo.MongoClient(MONGO_CONNECTION)
mydb = myclient['planet_db']
planet_col = mydb['planet_collection']

class Day(Resource):
    def get(self):
        return {}

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

api.add_resource(Planets, '/day/')
api.add_resource(Planets, '/planets/')
api.add_resource(Chat, '/chat/')