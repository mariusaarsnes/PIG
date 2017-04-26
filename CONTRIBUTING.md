(TODO: General guidelines for contributing. Getting started, e.g some pointers as to what is where.)

# Table of contents
1. [file structure](#FileStruct)
2. [setup](#Setup)
3. [Updating the database schema](#DatabaseSchema)

# General file structure of the project <a name="FileStruct"></a>
Most of the project is in the `pig` directory. 
Here you will find both the front-end and back-end code.
The files outside of `pig` are mostly files for making the website run, testing our code, and administrative stuff.

## Front-end
* `pig/static` holds all the images, javascript and css
* `pig/templates` holds all the html templates that are used for rendering the different sites.

## back-end
* `pig/db` is where the code for the db is, making it possible to create a connection to the DB on Heroku.
* `pig/db/databases.py` contains the class used to connect to the DB on Heroku.
* `pig/db/models.py` contains all the models needed to either fetch from or write to the DB.


* `pig/login` contains python code that handles login and registration.
* `pig/login/LoginHandler.py` handles login event
* `pig/login/RegistrationHandler.py` Handles a registration event
* `pig/login/User.py`


* `pig/scripts` contains code for different tasks done in the back-end.
* `pig/scripts/create_division.py` used to create an instance of division and saving it to the database.
* `pig/scripts/DbGetters.py` all the methods used for fetching data from the database.
* `pig/scripts/DivideGroupsToLeaders.py` used to divide the generated groups over the different team leaders who are signed up for the division
* `pig/scripts/encryption.py` used to encryption and decryption
* `pig/scripts/PartitionAlg.py` used to make groups out of all who have signed up for a division. It uses a version of the K-Means clustering algorithm.
* `pig/scripts/register_user.py`
* `pig/scripts/Tasks.py` ment to be the file where all methods that aren't fetching data from the database is. This is WiP.

# Setup of website <a name="Setup"></a>

To run the application you need:
* A web server to host the website and the database
* A web browser to access the website

Source code:
* https://github.com/mariiuus/PIG.git

Dependencies:
* Python 3.6.0 or newer
* Flask==0.12
* Flask-SQLAlchemy==2.1
* Jinja2==2.9.5
* psycopg2==2.6.2
* SQLAlchemy==1.1.5
* Werkzeug==0.11.15
* flask_login==0.4.0
* python-coveralls ==2.9.0
* coverage==4.3.4

Setup:
* Upload the source code to the server
* If the webserver does not do this automatically, upload all the dependencies. 
(Heroku does this by reading the contents of `requirements.txt.`)
* Set up the database on the server, in theory any database system can be used, 
but one using the PostgreSQL is preferred.
* On the server, run `run.py`

 

# Updating the database schema (destructive) <a name="DatabaseSchema"></a>
These instructions will delete the current schema with all its tables 
and redefine the schema with the definitions in `database.sql` (from `master`).

1. Make desired changes in `database.sql` and get it merged into `master`.
2. `heroku pg:psql`
  * `drop schema public cascade`
  * `create schema public`
  * `\i database.sql`
  * `\i database.sql`

We currently have to do `\i database.sql` twice because of circular references. You will first see errors about tables that don't exist, and then tables that already exist. This is ok.
