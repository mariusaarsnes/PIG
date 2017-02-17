import os
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return render_template('index.html')


