import pymongo
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_CONNECTION = os.getenv('MONGO_CONNECTION')
myclient = pymongo.MongoClient(MONGO_CONNECTION)
mydb = myclient['planet_db']
planet_col = mydb['planet_collection']

x = planet_col.delete_many({})