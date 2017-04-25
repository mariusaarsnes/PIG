# encoding=UTF-8

import sys
from flask import Flask, redirect, url_for, request, render_template, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from pig.login.LoginHandler import LoginHandler
from pig.login.RegistrationHandler import RegistrationHandler
from pig.scripts.CreateDivision import CreateDivision
import pig.scripts.Encryption as encryption

from pig.db.database import Database
from pig.scripts.DbGetters import DbGetters
from pig.scripts.Tasks import Tasks
from pig.scripts.RegisterUser import RegisterUser
from pig.scripts.PartitionAlg import PartitionAlg


app = Flask(__name__, template_folder='templates')

# Instatiating different classes that are used by the functions below.
database = Database(app)

from pig.db.models import *

pig_key = "supersecretpigkey"
app.secret_key = pig_key
login_manager = LoginManager()
login_manager.init_app(app)

login_handler, registration_handler = LoginHandler(database, User), RegistrationHandler(database, User)
division_creator = CreateDivision(database, Division, Parameter, NumberParam, EnumVariant)
LoginHandler, RegistrationHandler = LoginHandler(database, User), RegistrationHandler(database, User)

db_getters = DbGetters(
                database, User, Division, Group, Parameter, Value, NumberParam, EnumVariant,
                user_division, user_group, division_parameter, parameter_value, user_division_parameter_value)
tasks = Tasks(
    database, User, Division, Group, Parameter, Value, NumberParam, EnumVariant,
    user_division, user_group, division_parameter, parameter_value, user_division_parameter_value)

division_registrator = RegisterUser(database,User,Division,user_division, Value, Parameter)

partition_alg = PartitionAlg(database, db_getters)

#This code is being used by the login_manager to grab users based on their IDs. Thats how we identify which user we
#are currently dealing with
@login_manager.user_loader
def user_loader(user_id):
    return login_handler.get_user_with_id(user_id)

#The Functions below are used to handle user interaction with te web app. That is switching between pages
@app.route("/")
def hello():
    return redirect(url_for("home"))

@app.route("/apply_group", methods=['GET', 'POST'])
@login_required
def apply_group():
    if request.method == 'POST':
        if db_getters.is_registered_to_division(current_user.id, int(request.form["DivisionId"])):
            return render_template("message.html", user=current_user, header="Already registered", message="You are already registered for this division!")
        for (key, value) in request.form.items():
            if key.startswith("Parameter") and not key.startswith("ParameterSelect"):
                if value == "":
                    return render_template("message.html", user=current_user, header="No value", message="One of the input fields in the form was left empty")
                elif len(key[9:]) > 0:
                    if not tasks.verify_number_parameter_input(int(key[9:]), value):
                        return render_template("message.html", user=current_user, header="Out of range", message="One or more of the numbers you selected was out of the input range!")
        division_registrator.register_user(current_user, int(request.form['DivisionId']), "Student")
        division_registrator.register_parameters(current_user, request.form)
        return render_template("message.html", user=current_user, header="Success!", message="You successfully signed up to the division " + str(request.form['DivisionName']) + " as a student!")
    else:
        message = None
        arg = request.args.get("values")
        if not arg is None:
            decoded = encryption.decode(pig_key, arg)
            if decoded is not "":
                [div_name, div_id, div_role] = decoded.split(",")
                if db_getters.is_registered_to_division(current_user.id, div_id):
                    return render_template("message.html", user=current_user, header="Already registered", message="You are already registered for this division!")
                division = database.get_session() \
                        .query(Division) \
                        .filter(Division.id == div_id) \
                        .first()
                if division_registrator.is_division_creator(current_user, int(div_id)):
                    return render_template("message.html", user=current_user, header="Error!", message="You cannot register for your own division!")
                if int(div_role) == 0:
                    params = division.parameters
                    return render_template("apply_group.html", user=current_user, message=message, params=params, div_name=div_name, div_id=div_id)
                else:
                    division_registrator.register_user(current_user, division.id, "TA")
                    return render_template("message.html", user=current_user, header="Success!", message="You successfully signed up to the division " + str(division.name) + " as a TA!")
            return render_template("message.html", user=current_user, header="Invalid link", message="The link you provided is not valid!")
    return render_template("apply_group.html", user=current_user, message=None, params=None)

@app.route("/create_division", methods=['GET', 'POST'])
@login_required
def create_division():
    if request.method == 'POST':
        try:
            msg = division_creator.register_division(current_user.id, request.form)
        except Exception as e:
            msg = "An error happened internally, and the division was not created"

        if msg is None:
            msg = "Division created successfully"
        return render_template("message.html", user=current_user, header="Create division", message=msg)
    return render_template("create_division.html", user=current_user)

@app.route("/show_groups_leader")
@login_required
def show_groups_leader():
    divisions = db_getters.get_all_divisions_where_leader_for_given_user(current_user= current_user)
    return render_template("show_groups_leader.html", user=current_user, divisions = divisions)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = LoginHandler.get_user(request.form["Username"], request.form["Password"])
        if user is not None:
            login_user(user)
            if request.args.get("values") is not None:
                return redirect(url_for("apply_group", values=request.args.get("values")))
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
    return render_template('index.html', user=current_user)


@app.route("/show_divisions")
@login_required
def show_divisions():
    divisions_participating = db_getters.get_all_divisions_where_member_or_leader_for_given_user(current_user=current_user)
    divisions_created = db_getters.get_all_divisions_where_creator_for_given_user(current_user=current_user)
    leader_links, member_links = tasks.generate_links(pig_key,divisions_created)
    return render_template("show_divisions.html", user=current_user,
                           divisions_participating=divisions_participating, divisions_created=divisions_created, leader_links=leader_links, member_links=member_links)


@app.route("/show_all_students")
@login_required
def show_all_students():
    divisions_created = db_getters.get_all_divisions_where_creator_for_given_user(current_user=current_user)
    return render_template("show_all_students.html", divisions_created=divisions_created, user=current_user, students=db_getters.get_all_students(current_user, 1))


@app.route("/show_all_students_listed")
@login_required
def show_all_students_listed():
    if request.args.get("divisionId") is not None:
        return render_template("show_all_students_listed.html", user=current_user, user_groups=db_getters.get_user_groups(int(request.args.get("divisionId"))), students=db_getters.get_all_students(current_user, int(request.args.get("divisionId"))))
    return redirect(url_for("home"))

@app.route("/division_groups", methods=['GET', 'POST'])
@login_required
def show_groupless_users():
    if request.method == "POST":
        if request.args.get("divisionId") is not None:
            division_id = int(request.args.get("divisionId"))
            print("Running alg!", file=sys.stderr)
            try:
                partition_alg.create_groups(current_user, division_id)
            except:
                pass
            return redirect(url_for("show_groupless_users", divisionId=request.args.get("divisionId")))
    elif request.args.get("divisionId") is not None:
        division_id = int(request.args.get("divisionId"))
        if division_registrator.is_division_creator(current_user, division_id):
            # View page
            return render_template("division_groups.html",\
                    user=current_user,\
                    division_id = division_id,\
                    group_size = db_getters.get_division(division_id).group_size,\
                    groups=db_getters.get_groups(division_id),\
                    groupless_users=db_getters.get_groupless_users(division_id))
        else:
            pass # TODO: permission denied?
    return redirect(url_for("home"))

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
    if request.args.get("values") is not None:
        return redirect(url_for("login", values=request.args.get("values")))
    return redirect(url_for("login"))
