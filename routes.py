from flask import Flask, render_template, jsonify, request 
from __main__ import app
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client.testdb

db.playlists.drop()
# 더미데이터 초기화
for number in range(101):
    user = "user {0}".format(number)
    title = "{0}번째 playlist A".format(number),
    db.playlists.insert_one({
        'user': user,
        'title': title,
        'songs':[{'songname':'새삥 (Prod. ZICO) (Feat. 호미들)', 'artist':'지코 (ZICO)'},
        {'songname':'After LIKE ', 'artist':'IVE'},
        {'songname':'Attention', 'artist':'NewJeans'},
        {'songname':'11', 'artist':'111'},
        {'songname':'22', 'artist':'222'}
        ]})

# db.playlists.insert_one({
#     'user':'suyeon',
#     'title': '힙합 플레이리스트!',
#     'songs':[
#     {'songname':'가가가', 'artist':'나나나'}, 
#     {'songname':'asdf', 'artist':'efef'}, 
#     {'songname':'jklkj', 'artist':'seffew'}
#     ]})

@app.route('/')
def home():
    return render_template('index.html')


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

    result = list(db.songlists.find({}, {'_id': 0}).sort('like', -1))
    
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

    title_receive = request.form['title_give']
    song_receive = request.form['song_give']
    artist_receive = request.form['artist_give']
    time_receive = datetime.datetime.utcnow()

    addSong = {'songname': song_receive, 'artist': artist_receive, 'like': 0}

    target = db.playlists.find_one({'title': title_receive})
    target['songs'].append(addSong)
    
    db.playlists.update_one({'title': title_receive},{'$set':{'created_at':time_receive}})

    sameornot = db.songlists.find_one({'songname': song_receive}, {'artist': artist_receive})

    if sameornot is None :
        db.songlists.insert_one(addSong)
    else :
        new_like = sameornot['like'] + 1
        db.songlists.update_one({'songname': song_receive}, {'artist': artist_receive}, {'$set':{'like': new_like}})

    return jsonify ({'result': 'success'})


@app.route('/delete/song', methods=['POST'])
def deleteSong():

    title_receive = request.form['title_give']
    song_receive = request.form['song_give']
    artist_receive = request.form['artist_give']

    target = db.playlists.find_one({'title': title_receive})
    target['songs'].remove({'songname': song_receive, 'artist': artist_receive})
    
    return jsonify ({'result': 'success'})


@app.route('/search', methods=['GET', 'POST'])
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