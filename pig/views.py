# encoding=UTF-8

from flask import Flask, redirect, url_for, request, render_template
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from pig.login.login_handler import login_handler
from pig.login.registration_handler import registration_handler
from pig.scripts.create_division import create_division
import pig.scripts.encryption as encryption
from pig.scripts.get_divisions import get_divisions
from pig.db.database import database

app = Flask(__name__, template_folder='templates')

# Instatiating different classes that are used by the functions below.
database = database(app)

from pig.db.models import *

pig_key = "supersecretpigkey"
app.secret_key = "key"
login_manager = LoginManager()
login_manager.init_app(app)


login_handler, registration_handler = login_handler(database, User), registration_handler(database, User)
division_creator = create_division(database, Division, Parameter)
divisions_get = get_divisions(database, User)

#This code is being used by the login_manager to grab users based on their IDs. Thats how we identify which user we
#are currently dealing with
@login_manager.user_loader
def user_loader(user_id):
    return login_handler.get_user_with_id(user_id)

#The Functions below are used to handle user interaction with te web app. That is switching between pages

@app.route("/")
def hello():
    return render_template('index.html', user=current_user)

@app.route("/apply_group")
@login_required
def apply_group():
    return render_template("apply_group.html", user=current_user)

@app.route("/create_division", methods=['GET', 'POST'])
@login_required
def create_division():
    if request.method == 'POST':
        division_creator.register_division(current_user, request.form)
        return redirect(url_for("home"))
    return render_template("create_division.html", user=current_user)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = login_handler.get_user(request.form["Username"], request.form["Password"])
        if user is not None:
            login_user(user)
            return redirect(url_for("home"))
        else:
            return render_template("login.html", user=current_user, error=True)
    return render_template("login.html", user=current_user)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result = registration_handler.validate_form(request.form)
        if result[0]:
            registration_handler.create_user(request.form["FirstName"], request.form["LastName"], request.form["Email"], request.form["Password"])
            return redirect(url_for("login"))
        else:
            return render_template("register.html", user=current_user, error=result[1])
    return render_template("register.html", user=current_user)

@app.route("/home")
def home():
    return render_template("index.html", user=current_user)


@app.route("/show_divisions")
def show_divisions():
    divisions_participating, divisions_created, ta_links, student_links = divisions_get.fetch_divisions(current_user, pig_key)
    return render_template("show_divisions.html", user=current_user,
                           divisions_participating=divisions_participating, divisions_created=divisions_created, ta_links=ta_links, student_links=student_links)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/register_division")
def register_division():
    arg = request.args.get("values")
    if not arg is None:
        values = encryption.decode(pig_key, arg)
        variables = values.split(",")
        for i in range(0, len(variables)):
            variables[i] = variables[i].split(":")[1]
        return render_template("register_division.html", user=current_user, message="Successfully registered you for the group: " + variables[0] + " as a " + ("TA" if int(variables[2]) == 1 else "student"))
    return render_template("register_division.html", user=current_user)

@app.route("/404")
def not_found():
    return render_template("unauthorized.html", user=current_user)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("not_found"))
