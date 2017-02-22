from flask import Flask, request
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='templates')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
db = SQLAlchemy(app)

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

