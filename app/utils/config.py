import os
import logging
from dotenv import load_dotenv
import pymysql

# Load environment variables from .env file
load_dotenv(override=True)

# Set up basic logging
logging.basicConfig(level=logging.INFO)

class Config:
    _instance = None  # This holds the single instance of the class
    
    def __new__(cls):
        # If an instance doesn't already exist, create one
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Initialize configuration variables if not already initialized
        if not hasattr(self, '_initialized'):
            self.PORT = os.getenv('PORT', 5000)
            self.HOST = os.getenv('HOST', 'localhost') 
            self.DB_HOST = os.getenv('DB_HOST', 'localhost')
            self.DB_USER = os.getenv('DB_USER', 'root')
            self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
            self.DB_NAME = os.getenv('DB_NAME', 'devlinks')

    def get_db_connection(self):
        connection = pymysql.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            database=self.DB_NAME
        )
        return connection        