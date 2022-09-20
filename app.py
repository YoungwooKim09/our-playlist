from flask import Flask
from flask import Flask, render_template, jsonify, request 
app = Flask(__name__)

from pymongo import MongoClient

import routes

client = MongoClient('localhost', 27017)
db = client.testdb


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)