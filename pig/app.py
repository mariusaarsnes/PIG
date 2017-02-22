from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

test = models.users(firstName='firstTest', lastName='lastTest', email ='test@test.com', role='test')
db.session.add(test)
db.session.commit()


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/apply_group")
def apply_group():
    return render_template("apply_group.html")


@app.route("/create_division")
def create_division():
    return render_template("create_division.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("index.html")

