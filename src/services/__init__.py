import os

from pymongo import MongoClient

__all__ = ['mongo_client', 'database']

mongo_client = MongoClient(os.environ.get('DB_URL'))
database = mongo_client.get_database('ppob')
