from flask import Flask
app = Flask(__name__)

from pymongo import MongoClient

import routes

client = MongoClient('localhost', 27017)
db = client.testdb


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)