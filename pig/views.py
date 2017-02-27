# encoding=UTF-8

from flask import Flask, redirect, url_for, request, render_template
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from pig.login.LoginHandler import LoginHandler
from pig.login.RegistrationHandler import RegistrationHandler
from pig.db.Database import Database
from pig.scripts.CreateDivision import CreateDivision

app = Flask(__name__, template_folder='templates')

database = Database(app)

from pig.db.models import *
#Denne importen må ligge etter at vi lager databaseobjektet fordi klassene
#i model krever at det finnes en kjørende databaseinstans

app.secret_key = "key"
login_manager = LoginManager()
login_manager.init_app(app)

division_handler = CreateDivision(database, Division, Parameter)
login_handler, registration_handler = LoginHandler(database, User), RegistrationHandler(database, User)

@login_manager.user_loader
def user_loader(user_id):
    return login_handler.get_user_with_id(user_id)

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
        division_handler.register_division(current_user, request.form)
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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/404")
def not_found():
    return render_template("unauthorized.html", user=current_user)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("not_found"))