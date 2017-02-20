from flask import Flask, request
from flask import render_template
from flask.ext.mysql import MySQL

app = Flask(__name__, template_folder='templates')

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'mariaars_pu'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pu'
app.config['MYSQL_DATABASE_DB'] = 'sebasto_pig'
app.config['MYSQL_DATABASE_HOST'] = 'mysql.stud.ntnu.no'
mysql.init_app(app)

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

