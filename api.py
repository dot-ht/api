from tkinter.tix import Tree
from unittest import defaultTestLoader
from flask import Flask, request
from flask_restful import Resource, abort, Api
from marshmallow import Schema, fields
import pymongo
import os
import json

planets = {
    'planet_name': fields.String(allow_none=True),
    'planet_img': fields.String(allow_none=True),
    'planet_info': fields.String(allow_none=True)
}

# content = {
#     'answer_txt': fields.String(allow_none=True),
#     'cdn_img_ling': field
# }

bot_question = {
    'type': fields.String(allow_none=True),
}

app = Flask(__name__)
api = Api(app)

MONGO_CONNECTION = os.getenv('MONGO_CONNECTION')

myclient = pymongo.MongoClient(MONGO_CONNECTION)
mydb = myclient['planet_db']
planet_col = mydb['planet_collection']

PlanetSchema = Schema.from_dict(planets)
BotSchema = Schema.from_dict(bot_question)

class Planets(Resource):
    def get(self):
        request_data = request.get_json()
        
        errors = PlanetSchema().validate(request_data)
        print(errors)
        if errors:
            return {"planets": None}, 400
        
        
        
        mongo_query = planet_col.find()
        return_json = []
        for i in mongo_query:
            return_json.append(i)
        
        return {'planets': return_json}, 200

class Chat(Resource):
    def get(self):
        return {}

api.add_resource(Planets, '/planets/')
api.add_resource(Chat, '/chat/')