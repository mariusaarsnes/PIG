import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from pig.login.LoginManager import LoginManager as Login


app = Flask(__name__, template_folder='templates')
app.secret_key = "key"
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return Login.get_user_with_id(user_id)

#Det andre parameteret i render_template er parameter som blir brukt i selve html koden
#Er ikke lagt til noe ordentlig login system, dette er bare en test for å skjekke at ting fungerer
@app.route("/")
def hello():
    return render_template('index.html', user=current_user)

@app.route("/apply_group")
@login_required
def apply_group():
    return render_template("apply_group.html", user=current_user)

#Dersom det kommer en POST request vil metoden få inn en dict med alle verdiene i html formen. Dette vil da si tittel på
#divisjonen og alle parameterne.
@app.route("/create_division", methods=['GET', 'POST'])
@login_required
def create_division():
    if request.method == 'POST':
        pass
        #TODO - Ta parameterne man får inn her og legge dem inn i databasen
    return render_template("create_division.html", user=current_user)

#Dersom det kommer en POST request vil metoden faa inn en dict med alle verdiene i html formen. Gjorde bare en liten test
#for å endre side (og sette login variabelen til logged in)
@app.route("/login", methods=['GET', 'POST'])
def login():
    #TODO - Need to implement a login manager to keep track of sessions
    if request.method == 'POST':
        user = Login.get_user(request.form["Username"], request.form["Password"])
        if user is not None:
            login_user(user)
            return redirect(url_for("home"))
        else:
            return render_template("login.html", user=current_user, error=True)
    return render_template("login.html", user=current_user)

@app.route("/home")
def home():
    return render_template("index.html", user=current_user)

#Bare satte logged_in til false for å teste
@app.route("/logout")
@login_required
def logout():
    #TODO - Need to implement a login manager to keep track of sessions
    logout_user()
    return redirect(url_for("home"))

@app.route("/404")
def not_found():
    return render_template("unauthorized.html", user=current_user)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("not_found"))