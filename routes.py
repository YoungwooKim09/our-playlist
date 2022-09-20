from flask import render_template, jsonify, request 
from __main__ import app

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

import datetime

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/list/all', methods=['GET'])
def listAllplaylists():

    result = list(db.playlists.find({}, {'_id': 0}))
    
    return jsonify ()

@app.route('/add/playlist', methods=['POST'])
def addPlaylist():

    user_receive = request.form['user_give']
    title_receive = request.form['title_give']
    songs = {}
    playlist = {'user': user_receive, 'title': title_receive, 'songs': songs, 'time_receive' : 0}

    db.playlists.insert_one(playlist)

    return jsonify ({'result': 'success'})

@app.route('/add/song', methods=['POST'])
def addSong():

    song_receive = request.form['song_give']
    artist_receive = request.form['artist_give']
    time_receive = datetime.datetime.utcnow()

    songs = {'songname' : song_receive, 'singer' : artist_receive}
    playlists = playlists.append(songs)
    # time_receive 업데이트
    # songs 딕셔너리 추가
    


@app.route('/search', methods=['POST'])
def searchList():

    search_receive = request.form['search_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://www.melon.com/search/total/index.htm?q=${search_receive}&section=&mwkLogType=T', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    search_song_list = soup.select('#frm_searchSong tbody > tr > td.t_left div.ellipsis > a.fc_gray')
    search_song_name = list(search_song_list.text)

    return jsonify ({'result': 'success'}, {'search_song_name_list': search_song_name})