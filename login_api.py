from __main__ import app
from datetime import datetime, timedelta
from flask import render_template, jsonify, request 
import hashlib
from pymongo import MongoClient
import jwt
client = MongoClient('localhost', 27017)
db = client.accountdb

SECRET_KEY = 'WOOPLY'

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/api', methods=['POST'])
def api_login():
    print('hello??')
    id_rec = request.form['id_return']
    pw_rec = request.form['pw_return']
    print(id_rec, pw_rec)
    pw_hash = hashlib.sha256(pw_rec.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id' : id_rec, 'pw' : pw_hash})
    print(result)
    if result is not None:
        payload = {
            'id' : id_rec,
            'exp' : datetime.utcnow() + timedelta(seconds=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result' : 'success', 'msg' : result['name'] + '님 환영합니다.', 'token' : token})
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
