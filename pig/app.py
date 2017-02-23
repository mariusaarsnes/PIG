# encoding=UTF8

from flask import Flask, redirect, url_for, request, render_template
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

from pig.login.LoginManager import LoginManager as Login


app = Flask(__name__, template_folder='templates')
app.secret_key = "key"
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://wtsceqpjdsbhxw:34df69f4132d39ea5b95e52822d6dedc8e3eb368915cb8888526f896f21bce75@ec2-54-75-229-201.eu-west-1.compute.amazonaws.com:5432/dfa7tvu04d7t6i"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from pig import models

# Er er det noen eksempler på sporringer til databasen.
#
#print(db.session.query(models.User).filter(models.User.firstname == "Marius").first().lastname)
#print(db.session.query(User).all())
#users = db.session.query(User).all()
#print(users[0].firstname)