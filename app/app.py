#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import sqlite3

from flask import Flask, request
from flask_cors import CORS
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)
import ujson as json
from bcrypt import checkpw

from user import User
from secret import DB_FILENAME, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
CORS(app, supports_credentials=True)


@login_manager.user_loader
def load_user(user_id):
    query = 'SELECT email, pw_hash FROM users WHERE email=?'
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute(query, (user_id, ))
    row = c.fetchone()
    conn.close()
    if not row:
        return
    email = row[0]
    pw_hash = row[1]
    return User(email, pw_hash)


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return 'OK'
    login_request = request.get_json()
    email = login_request.get('email')
    if not email:
        return 'Not authorized', 401
    user = load_user(email)
    if not user or 'pw' not in login_request:
        return 'Not authorized', 401
    pw = login_request.get('pw').encode('utf-8')
    if checkpw(pw, user.pw_hash):
        login_user(user, remember=True)
        return 'OK'
    else:
        return 'Not authorized', 401


def verify_login(user_dict) -> bool:
    return False


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    return 'Hello, world!'


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return 'OK'


@app.route('/todo', methods=['POST', 'GET'])
@login_required
def todo():
    if request.method == 'POST':
        new_item_id = add(request.get_json())
        return new_item_id
    elif request.method == 'GET':
        return json.dumps(get_all())
    else:
        raise ValueError('Unexpected request method')
    todo_uuid = str(uuid.uuid1())
    return json.dumps([todo_uuid])


@app.route('/todo/<item_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def todo_item(item_id: str):
    if request.method == 'GET':
        result = json.dumps(get_one(item_id))
    elif request.method == 'PUT':
        update(request.get_json())
    elif request.method == 'DELETE':
        delete(item_id)
    else:
        raise ValueError('Unexpected request method')
    item_id = str(uuid.uuid1())
    return json.dumps([item_id])


def add(form):
    item_id = str(uuid.uuid1())
    content = form['content']
    query = 'INSERT INTO todos (uuid, content) VALUES (?,?)'
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute(query, (item_id, content))
    conn.commit()
    conn.close()
    return item_id


def update(form):
    item_id = form['itemId']
    content = form['content']
    is_done = form['isComplete']
    query = 'UPDATE todos SET content=?, is_done=? WHERE uuid=?'
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute(query, (content, is_done, item_id))
    conn.commit()
    conn.close()
    return item_id


def get_all():
    query = 'SELECT uuid, content, is_done, time_create, time_edit FROM todos'
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute(query)
    result = list()
    for row in c.fetchall():
        result += [row_to_obj(row)]
    conn.close()
    return result


def get_one(item_id: str):
    query = 'SELECT uuid, content, is_done, time_create, time_edit FROM todos WHERE uuid=?'
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute(query, (item_id, ))
    result = c.fetchone()
    conn.close()
    return row_to_obj(result)


def delete(item_id: str):
    query = 'DELETE FROM todos WHERE uuid=?'
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute(query, (item_id, ))
    conn.commit()
    conn.close()


def row_to_obj(row):
    return {
        'itemId': row[0],
        'content': row[1],
        'isComplete': row[2] > 0,
        'timeCreate': row[3],
        'timeEdit': row[4],
    }


def add_user(email, pw):
    from bcrypt import gensalt, hashpw

    salt = gensalt()
    pw_hash = hashpw(pw.encode('utf-8'), salt)

    query = 'INSERT INTO users (email, pw_hash) VALUES (?,?)'
    conn = sqlite3.connect(DB_FILENAME)
    c = conn.cursor()
    c.execute(query, (email, pw_hash))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
