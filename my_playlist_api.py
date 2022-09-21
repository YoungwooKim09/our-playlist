from flask import Flask, render_template, jsonify, request 
from __main__ import app
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.testdb

@app.route('/my-playlist')
def renderMyPlaylist(user_id = None):
    if user_id is not None:
        print(11111)
        playlists = list(db.playlists.find({'user': user_id}, {'_id': 0}))
        return render_template('myplaylist.html', playlists = playlists)
    else:
        print(22222)
        return render_template('myplaylist.html', playlists=[1,2,3,4])

