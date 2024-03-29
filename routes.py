from flask import Flask, render_template, jsonify, request 
from __main__ import app
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client.testdb

@app.route('/')
def home():
    playlists = list(db.playlists.find({}, {'_id': 0}).limit(10))
    print(playlists)
    return render_template('index.html', playlists = playlists)

@app.route('/list/all', methods=['GET'])
def listAllplaylists():
    page = request.args.get('page')
    if  page != None:
        page = int(page) 
        foundElements = list(db.playlists.find({}, {'_id': 0}).skip((int(page) - 1) * 10).limit(10))
        return jsonify ({'result': 'success', 'all_playlists': foundElements})
    else:
        foundElements = list(db.playlists.find({}, {'_id': 0}).sort('created_at', -1))
        return jsonify ({'result': 'success', 'all_playlists': foundElements})


@app.route('/list/popular', methods=['GET'])
def listPopularlists():
    
    popular_playlists = list(db.songslists.find({}, {'_id': 0}).sort('like', -1))

    return jsonify ({'result': 'success', 'popular_playlists': popular_playlists})


@app.route('/add/playlist', methods=['POST'])
def addPlaylist():
    title = request.form['title']
    user = request.form['user']
    username = request.form['username']

    playlist = {'user': user, 'username': username, 'title': title, 'songs' : [], 'created_at' : 0}
    db.playlists.insert_one(playlist)

    return jsonify ({'result': 'success'})

@app.route('/list/myplaylist', methods=['GET'])
def listMyplaylist():
    user_id = request.args.get('user_id')
    playlists = list(db.playlists.find({'user_id': user_id}, {'_id': 0}))
    # return render_template('myplaylist.html', playlists = playlists)
    return jsonify ({'result': 'success', 'list_myplaylist': playlists})

@app.route('/delete/playlist', methods=['POST'])
def deletePlaylist():

    id = ObjectId(request.form['id'])
    print(id)
    db.playlists.delete_one({'_id': id})

    return jsonify ({'result': 'success'})


@app.route('/add/song', methods=['POST'])
def addSong():

    song_receive = request.form['song_give']
    artist_receive = request.form['artist_give']
    id_receive = ObjectId(request.form['id_give'])
    time_receive = datetime.datetime.utcnow()

    addSong = {'songname': song_receive, 'artist': artist_receive}
    print(addSong)
    print(id_receive)
    target = db.playlists.find_one({'_id': id_receive})
    print(target)
    t = target['songs']
    t.append(addSong)
    db.playlists.update_one({'_id': id_receive},{'$set': {'songs': t}})
    
    print('last call', db.playlists.find_one({'_id' : id_receive}))
    # db.playlists.update_one({'_id': id_receive},{'$set':{'created_at':time_receive}})

    # sameornot = db.songslists.find_one({'songname': song_receive}, {'artist': artist_receive})
    
    # if sameornot is None :
    #     db.songslists.insert_one(addSong)
    # else :
    #     new_like = sameornot['like'] + 1
    #     db.songslists.update_one({'songname': song_receive}, {'artist': artist_receive}, {'$set':{'like': new_like}})

    return jsonify ({'result': 'success'})


@app.route('/delete/song', methods=['POST'])
def deleteSong():

    title_receive = request.form['title_give']
    song_receive = request.form['song_give']
    artist_receive = request.form['artist_give']

    target = db.playlists.find_one({'title': title_receive})
    target['songs'].remove({'songname': song_receive, 'artist': artist_receive})
    
    return jsonify ({'result': 'success'})


@app.route('/search', methods=['GET','POST'])
def searchList():

    search_receive = request.form['search_give']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://www.melon.com/search/total/index.htm?q='+search_receive+'&section=&mwkLogType=T', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    search_song_list = soup.select('tbody > tr')
    song_list = []
    for songs in search_song_list :
        song_list.append({
            'song_name' :  songs.select_one('td.t_left > div.wrap.pd_none > div.ellipsis > a.fc_gray').text,
            'song_singer' : songs.select_one('#artistName > a').text
        })
    return jsonify ({'result': 'success', 'song' : song_list})
    # '노래 제목 : 가수' 형태로 데이터 전달 구현
