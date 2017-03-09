__author__ = 'owner_000'

from flask_sqlalchemy import SQLAlchemy

#Class that handles the database connection
class database:

    def __init__(self, app):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://wtsceqpjdsbhxw:34df69f4132d39ea5b95e52822d6dedc8e3eb368915cb8888526f896f21bce75@ec2-54-75-229-201.eu-west-1.compute.amazonaws.com:5432/dfa7tvu04d7t6i"
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.db = SQLAlchemy(self.app)


    def set_uri(self,value):
        self.app.config['SQLALCHEMY_DATABASE_URI'] = value

    def get_session(self):
        return self.db.session