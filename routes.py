from flask import Flask, render_template, jsonify, request 
from __main__ import app
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client.testdb


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/list/all', methods=['GET'])
def listAllplaylists():

    result = list(db.playlists.find({}, {'_id': 0}))
    
    return jsonify ({'result': 'success', 'all_playlists': result})


@app.route('/list/popular', methods=['GET'])
def listPopularlists():

    result = list(db.playlists.find({}, {'_id': 0}))
    
    return jsonify ({'result': 'success', 'popular_playlists': result})


@app.route('/add/playlist', methods=['POST'])
def addPlaylist():

    user_receive = request.form['user_give']
    title_receive = request.form['title_give']
    song_receive = []
    playlist = {'user': user_receive, 'title': title_receive, 'songs': song_receive, 'created_at' : 0}

    db.playlists.insert_one(playlist)

    return jsonify ({'result': 'success'})


@app.route('/delete/playlist', methods=['POST'])
def deletePlaylist():

    delete_receive = request.form['delete_give']
    db.playlists.delete_one({'title': delete_receive})

    return jsonify ({'result': 'success'})


@app.route('/add/song', methods=['POST'])
def addSong():

    song_receive = request.form['song_give']
    artist_receive = request.form['artist_give']
    time_receive = datetime.datetime.utcnow()

    addSong = {'songname': song_receive, 'artist': artist_receive}
    playlists = playlists['songs'].append(addSong)
    
    db.playlists.update_one({'user': 'user_receive'},{'$set':{'created_at':time_receive}})
    # 해당 Playlist 특정 기능


@app.route('/search', methods=['POST'])
def searchList():

    search_receive = request.form['search_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://www.melon.com/search/total/index.htm?q=${search_receive}&section=&mwkLogType=T', headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    search_song_list = soup.select('#frm_searchSong tbody > tr > td.t_left div.ellipsis > a.fc_gray')
    search_artist_list = soup.select('#artistName > a')

    search_song_name = list(search_song_list.text)
    search_song_artist = list(search_artist_list.text)

    return jsonify ({'result': 'success'}, {'search_song_name_list': search_song_name})
    # '노래 제목 : 가수' 형태로 데이터 전달 구현