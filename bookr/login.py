from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from bookr.app import app, query_db, get_db
from bookr.validation import get_session


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the login on the site. Returns to main menu if the user is already logged in. If not, sets the session data
    and redirects to the main menu.

    Doesn't do a check if the username is correct, but the password is wrong. It really should though!

    :return: Redirects to the main menu as a logged in user.
    """
    error = None
    if get_session() is True:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']
        user = query_db('SELECT * FROM Users WHERE username = ? AND password = ?', (username_form, password_form))
        if user:
            session['logged_in'] = True
            session['session_username'] = username_form
            session['session_role'] = user[0][3]
            return redirect(url_for('index'))
        else:
            error = "Brukernavn eller passord er inkorrekt."
            return render_template('user_login.html', error=error)
    else:
        return render_template('user_login.html')


@app.route('/logout')
def logout():
    """
    Clears the session data, redirects you back to the login page.
    :return: Login page (see forms)
    """
    if request.method == 'GET':
        session.clear()
        return render_template('user_login.html')


@app.route('/register')
def register_user():
    """
    Redirects to the page for registering users. Also stops logged in users from registering anew.
    :return: Main menu if you're already logged in, register page if not
    """
    error = None
    if get_session():
        return redirect(url_for('index'))
    else:
        return render_template("user_register.html")


@app.route('/registration_handler', methods=['POST'])
def registration_handler():
    """
    Registers a user and logs them in if all is clear. If the username is taken already, re-render the page with error
    :return: Redirects to main menu and logs in when successfully registered.
    """
    error = None
    username_form = request.form['username']
    password = request.form['password']
    role = request.form['roles']
    if query_db('SELECT * FROM Users WHERE username = ?', (username_form,)):
        error = "The username is already taken"
        return render_template("user_register.html", error=error)
    else:
        get_db().execute("INSERT INTO Users (username,password,role) VALUES (?,?,?)", (username_form, password, role))
        g._database.commit()
        session['logged_in'] = True
        session['session_role'] = role
        session['session_username'] = username_form
        return redirect(url_for('index'))
