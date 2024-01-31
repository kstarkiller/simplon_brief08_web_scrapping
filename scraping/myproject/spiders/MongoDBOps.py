
from pymongo import MongoClient

class MongoDBManager:
    def __init__(self):
        self.client = MongoClient('mongodb://127.0.0.1:27017/')
        self.db = self.client['biblio']
        self.collection = self.db['books']

    def store_in_mongodb(self, book_data):
        # Insert data into the collection
        self.collection.insert_one(book_data)

    def read_from_mongodb(self):
        # Add read operations if needed
        pass
