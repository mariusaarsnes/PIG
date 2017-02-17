import os
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

app = Flask(__name__, template_folder='templates')

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("apply_group")
def apply_group():
    return render_template("apply_group")
@app.route("create_division")
def create_division():
    return render_template("create_division")


