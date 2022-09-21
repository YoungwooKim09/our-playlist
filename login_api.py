from __main__ import app
from datetime import datetime, timedelta
from functools import wraps
from xmlrpc.client import ResponseError
from flask import render_template, jsonify, request, redirect, url_for, Response, current_app
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
import hashlib
from pymongo import MongoClient
import time
import jwt

bcrypt = Bcrypt(app)
client = MongoClient('localhost', 27017)
db = client.accountdb
testdb = client.testdb
SECRET_KEY = 'WOOPLY'

# @login_confirm
# def action():
#     print('login confirm')
#     return redirect(url_for('/'))

def check_access_token(access_token):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, 'HS256')
        print(payload['exp'], time.time)
        if payload['exp'] < time.time():
            payload = None
    except jwt.InvalidTokenError:
        payload = None
    return payload

def login_confirm(f):
    @wraps(f)
    def deco_func(*args, **kwagrs):
        access_token = request.headers.get('Cookie')
        # print(access_token)
        if access_token is not None:
            payload = check_access_token(access_token.split("; ")[1])
            if payload is None:
                return render_template('login.html')
        else:
            return render_template('login.html')
        return f(*args, **kwagrs)
    return deco_func

# @login_confirm
# def action():
#     print('login confirm')
#     return redirect(url_for('/'))


@app.route('/login')
@login_confirm
def api_():
    return redirect(url_for('home'))

@app.route('/my-playlist')
@login_confirm
def playlist():
    cookie = request.headers.get('Cookie')
    print('cookie', cookie)
    if cookie is not None:
        playlists = list(testdb.playlists.find({'user': cookie.split('"id":')[1].split(',')[0].split('"')[1]}))
        print(playlists)
        return render_template('myplaylist.html', playlists = playlists)
    else:
        return render_template('myplaylist.html')


@app.route('/login/api', methods=['POST'])
def api_login():
    print('hello??')
    id_rec = request.form['id_return']
    pw_rec = request.form['pw_return']
    pw_hash = hashlib.sha256(pw_rec.encode('utf-8')).hexdigest()
    result = db.user.find_one({'id' : id_rec, 'pw' : pw_hash})
    if result is not None:
        payload = {
            'id' : id_rec,
            'exp' : datetime.utcnow() + timedelta(seconds=6000)
        }
        print(payload['exp'])
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        user_info = {'name' : result['name'], 'id' : result['id']}
        return jsonify({'result' : 'success', 'msg' : result['name'] + '님 환영합니다.','token' : token, 'info' : user_info})
    else:
        return jsonify({'result' : 'success', 'msg' : "아이디/비밀번호가 일치하지 않습니다."})


@app.route('/login/register', methods=['POST'])
def api_resgister():
    id_rec = request.form['id_return']
    pw_rec = request.form['pw_return']
    name_rec = request.form['name_return']
    # 해쉬되는 부분 다시 공부할것 
    pw_hashed = hashlib.sha256(pw_rec.encode('utf-8')).hexdigest()
    registered_user = db.user.find_one({'id':id_rec})
    print(registered_user)
    if registered_user is not None:
        return jsonify({'result' : 'fail'})
    else:
        db.user.insert_one({'id' : id_rec, 'pw' : pw_hashed, 'name' : name_rec})
        return jsonify({'result' : 'success'})
