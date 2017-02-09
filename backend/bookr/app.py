# encoding=utf8

import sqlite3

from flask import Flask
from flask import g

# App declaration
app = Flask(__name__, template_folder='templates')

# Updates app with config from config.py
app.config.from_object('config')


def get_db():
    """
    Connects Flask to the database
    :return:
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db


@app.teardown_appcontext
def close_connection(exception):
    """
    Close the connection to the database.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """
    Send Query-requests with arguments to the SQLite database, fetches the data and returns it.
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
