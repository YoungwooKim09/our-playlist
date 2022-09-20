from datetime import datetime
from distutils.debug import DEBUG
from email.mime import application
import hashlib, datetime
from flask import Flask, render_template, jsonify, request 
from flask_jwt_extended import *

app = Flask(__name__)

import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.testdb


#  temp secretkey

SECRET_KEY = 'WOOPLY'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('login/api')
def api_login():
    id_rec = request.form['id_return']
    pw_rec = request.form['pw_return']

    pw_hash = hashlib.sha256(pw_rec.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id' : id_rec , 'pw' : pw_hash})
    if result is not None:
        payload = {
            'id' : id_rec,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds = 5)
        }
        # exp 기한 설정이 어떻게 되고 어떤 의미를 갖는지 공부할 것 
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        jwt.jwt_encode_handler()
        return jsonify({'result' : 'success', 'token' : token})
    else:
        return jsonify({'sesult' : 'fail', 'msg' : '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')
@app.route('/sign_in/register', methods=['POST'])
def api_resgister():
    id_rec = request.form['id_return']
    pw_rec = request.form['pw_return']
    name_rec = request.form['name_return']
    # 해쉬되는 부분 다시 공부할것 
    pw_hash = hashlib.sha256(pw_rec.encode('utf-8')).hexdigest()

    db.user.insert_one({'id' : id_rec, 'pw' : pw_hash, 'nick' : name_rec})
    return jsonify({'result' : 'successs'})
def register()
if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)