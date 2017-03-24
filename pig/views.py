# encoding=UTF-8

from flask import Flask, redirect, url_for, request, render_template, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from pig.login.LoginHandler import LoginHandler
from pig.login.RegistrationHandler import RegistrationHandler
from pig.scripts.create_division import Task_CreateDivision
import pig.scripts.encryption as encryption
from pig.scripts.GetStudents import GetStudents
from pig.scripts.register_user import Task_RegisterUser
from pig.db.database import Database
from pig.scripts.DbGetters import DbGetters
from pig.scripts.Tasks import Tasks


app = Flask(__name__, template_folder='templates')

# Instatiating different classes that are used by the functions below.
database = Database(app)

from pig.db.models import *


pig_key = "supersecretpigkey"
app.secret_key = pig_key
login_manager = LoginManager()
login_manager.init_app(app)

login_handler, registration_handler = LoginHandler(database, User), RegistrationHandler(database, User)
division_registrator = Task_RegisterUser(database, User, Division, user_division)
division_creator = Task_CreateDivision(database, Division, Parameter, NumberParam, EnumVariant)
get_students = GetStudents(database, Division, user_division, User)
LoginHandler, RegistrationHandler = LoginHandler(database, User), RegistrationHandler(database, User)

division_creator = Task_CreateDivision(database, Division, Parameter, NumberParam, EnumVariant)
division_registrator = Task_RegisterUser(database, User, Division, user_division)
db_getters = DbGetters(
                database, User, Division, Group, Parameter, Value, NumberParam, EnumVariant,
                user_division, user_group, division_parameter, parameter_value, user_division_parameter_value)
tasks = Tasks()

#This code is being used by the login_manager to grab users based on their IDs. Thats how we identify which user we
#are currently dealing with
@login_manager.user_loader
def user_loader(user_id):
    return LoginHandler.get_user_with_id(user_id)

#The Functions below are used to handle user interaction with te web app. That is switching between pages
@app.route("/")
def hello():
    return redirect(url_for("home"))

@app.route("/apply_group", methods=['GET', 'POST'])
@login_required
def apply_group():
    # TODO split into separate module
    message = None
    arg = request.args.get("values")
    if not arg is None:
        [div_name, div_id, div_role] = encryption.decode(pig_key, arg).split(",")
        division = database.get_session() \
                .query(Division) \
                .filter(Division.id == div_id) \
                .first()
        if division_registrator.is_division_creator(current_user, div_id):
            message = "You cannot register for your own division!"

        elif int(div_role) == 1:
            division_registrator.register_user(current_user, div_id, "Leader")
            message = "Successfully registered you as a leader in the division: " + div_name
        if request.method == 'POST':
            return redirect(url_for("home"))
            # TODO Actually register the person
            """
            if int(div_role) == 0:
                return render_template("apply_group.html", user=current_user,\
                        message="Successfully registered you as a TEAM MEMBER for the division: " + div_name)
            elif int(div_role) == 1:
                return render_template("apply_group.html", user=current_user,\
                        message="Successfully registered you as a LEADER for the division: " + div_name)
            """
        else:
            # Make the form
            #params = division.parameters
            return render_template("apply_group.html", user=current_user, message=message, params=None, div_name=div_name)

    return render_template("apply_group.html", user=current_user, message=None, params=None)

@app.route("/create_division", methods=['GET', 'POST'])
@login_required
def create_division():
    if request.method == 'POST':
        try:
            msg = division_creator.register_division(current_user, request.form)
        except:
            msg = "An error happened internally, and the division was not created"

        if msg is None:
            msg = "Division created successfully"

        return render_template("message.html", user=current_user, message=msg)
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
            flash('You were logged in')
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
    print(get_students.get_all_students(current_user, 86))
    print(get_students.get_all_divisions_where_creator_for_given_user(current_user))
    return render_template("show_all_students.html", user=current_user, students=get_students.get_all_students(current_user, 86))

@app.route("/division_groups")
@login_required
def show_groupless_users():
    if request.args.get("divisionId") is not None:
        if division_registrator.is_division_creator(current_user, int(request.args.get("divisionId"))):
            return render_template("division_groups.html", user=current_user, groups=db_getters.get_groups(int(request.args.get("divisionId"))), groupless_users=db_getters.get_groupless_users(int(request.args.get("divisionId"))))
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
    return redirect(url_for("login"))
