# db.py
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        if not uri:
            raise ValueError("MONGODB_URI must be provided")

        self.uri = uri
        self.db_name = db_name
        self.client: MongoClient | None = None
        self.database = None

    def connect(self):
        """Initialize MongoDB client."""
        if self.client is not None:
            return  
        self.client = MongoClient(self.uri, server_api=ServerApi("1"))
        self.database = self.client[self.db_name]
        print("MongoDB connected")

    def close(self):
        """Close MongoDB connection cleanly."""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

    def get_collection(self, name: str):
        if self.database is None:
            self.connect()
        return self.database[name]


# Load environment
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_NAME = os.getenv("MONGODB_NAME")

mongodb = MongoDB(MONGODB_URI, MONGODB_NAME)