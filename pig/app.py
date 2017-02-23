from flask import Flask, redirect, url_for, request, render_template
from pig.wrapper import wrapper
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

wrapper = wrapper() #Denne klassen gjør egentlig ingenting, bare en testklasse der jeg la til en variabel
#som kan hentes fra html siden - Bare å fjerne dersom noen starter på et ordentlig login system

#Det andre parameteret i render_template er parameter som blir brukt i selve html koden
#Er ikke lagt til noe ordentlig login system, dette er bare en test for å skjekke at ting fungerer
@app.route("/")
def hello():
    return render_template('index.html', logged_in=wrapper.logged_in)

@app.route("/apply_group")
def apply_group():
    return render_template("apply_group.html", logged_in=wrapper.logged_in)

#Dersom det kommer en POST request vil metoden få inn en dict med alle verdiene i html formen. Dette vil da si tittel på
#divisjonen og alle parameterne.
@app.route("/create_division", methods=['GET', 'POST'])
def create_division():
    if request.method == 'POST':
        #TODO - Ta parameterne man får inn her og legge dem inn i databasen
        for k in request.form:
            print(k + ": " + request.form[k])
    return render_template("create_division.html", logged_in=wrapper.logged_in)

#Dersom det kommer en POST request vil metoden få inn en dict med alle verdiene i html formen. Gjorde bare en liten test
#for å endre side (og sette login variabelen til logged in)
@app.route("/login", methods=['GET', 'POST'])
def login():
    #TODO - Need to implement a login manager to keep track of sessions
    if request.method == 'POST':
        print("Received a login request (" + request.form["Username"] + ", " + request.form["Password"] + ")!")
        if request.form["Username"] == "daniel" and request.form["Password"] == "test":
            wrapper.logged_in = True
            return redirect(url_for("home"))
        else:
            return render_template("login.html", logged_in=wrapper.logged_in)
    else:
        return render_template("login.html", logged_in=wrapper.logged_in)

@app.route("/home")
def home():
    return render_template("index.html", logged_in=wrapper.logged_in)

#Bare satte logged_in til false for å teste
@app.route("/logout")
def logout():
    #TODO - Need to implement a login manager to keep track of sessions
    wrapper.logged_in = False
    return redirect(url_for("home"))