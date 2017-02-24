from pig.app import db


class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), unique = False)
    lastname = db.Column(db.String(255), unique = False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique =False)
    divisions_created = db.relationship("Division", backref='users')
    groups = db.relationship('Group', backref='users')

    def __repr__(self):
        return "ID: " + str(self.id) + ", name: " + str(self.firstname)+str(self.lastname)+ ", Email: " + str(self.email)

class Division(db.Model):
    __tablename__="divisions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    groups = db.relationship('Group',backref='divisions')



    def __repr__(self):
        return "ID: " + str(self.id) + ", name: " + str(self.name)+ ", creator: " + str(self.creator_id)


 # Helper table to get the role of a user in a division
users_divisions = db.Table('users_divisions',
                           db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
                           db.Column('division_id', db.Integer,db.ForeignKey('divisions.id')),
                           db.Column('role',db.String(255))
)

"""
class User_Division(db.Model):
    __tablename__="users_divisions"
    userID = db.Column(db.Integer, primary_key=True)
    divisionID = db.Column(db.Integer,primary_key=True)
    role = db.Column(db.String(255))

    def __repr__(self):
        return "userID: " + str(self.userID) + ", divisionID: " + str(self.divisionID) + ", users role: " + str(self.role)

"""


class Group(db.Model):
    __tablename__="groups"
    id = db.Column(db.Integer, primary_key=True)
    division_id = db.Column(db.Integer, db.ForeignKey('divisions.id'))
    leader_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "ID: " + str(self.id) + ", divisionID: " + str(self.division_id) + ", leader: " + str(self.leader_id)

users_groups = db.Table('users_groups',
                        db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
                        db.Column('group_id',db.Integer,db.ForeignKey('groups.id'))
)

"""
class User_Group(db.Model):
    __tablename__="users_groups"
    userID = db.Column(db.Integer,primary_key=True)
    groupID = db.Column(db.Integer,primary_key=True)

    def __repr__(self):
        return "userID: " + str(self.userID) + ", groupID: " + str(self.groupID)
"""

class Parameter(db.Model):
    __tablename__="parameters"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return "ID: " + str(self.id) + ", description: " + str(self.description)


class Value(db.Model):
    __tablename__="values"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    description = db.Column(db.String(255))

    def __repr__(self):
        return "ID: " + str(self.id) + ", description: " + str(self.description)

parameters_values= db.Table('parameters_values',
                            db.Column('parameter_id',db.Integer,db.ForeignKey('parameters.id')),
                            db.Column('value_id',db.Integer,db.ForeignKey('values.id'))
)

"""
class Parameter_Value(db.Model):
    __tablename__ = "parameters_values"
    parameterID = db.Column(db.Integer, primary_key=True)
    valueID = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "parameterID: " + str(self.parameterID) + ", valueID: " + str(self.valueID)
"""

users_divisions_parameters_values = db.Table('users_divisions_parameters_values',
                                             db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
                                             db.Column('division_id',db.Integer,db.ForeignKey('division.id')),
                                             db.Column('parameter_id',db.Integer,db.ForeignKey('parameters.id')),
                                             db.Column('value_id',db.Integer, db.ForeignKey('values.id'))
)

"""
class User_Division_Parameter_Value(db.Model):
    __tablename__ = "users_divisions_parameters_values"
    userID = db.Column(db.Integer, primary_key=True)
    divisionID = db.Column(db.Integer, primary_key=True)
    parameterID = db.Column(db.Integer, primary_key=True)
    valueID = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "userID: " + str(self.parameterID) + ", divisionID: " + str(self.valueID) +\
               "parameterID: " + str(self.parameterID) + ", valueID: " + str(self.valueID)
"""



