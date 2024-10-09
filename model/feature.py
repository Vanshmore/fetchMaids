from datetime import datetime
import pymongo
import pandas as pd
from bson.objectid import ObjectId
from geopy.distance import geodesic

# MongoDB connection string
mongo_uri = "mongodb+srv://morevansh2003:maideasy@cluster0.da2a1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(mongo_uri)

# Access the 'test' database
db = client['test']

