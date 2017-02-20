from flask import Flask
from flask import render_template
import mysql.connector


cnx = mysql.connector.connect(user='mariaars_pu', password='pu',
                              host='mysql.stud.ntnu.no',
                              database='sebasto_pig')
cnx.close()

app = Flask(__name__, template_folder='templates')

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

