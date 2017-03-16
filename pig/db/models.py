from pig.views import database as database

db = database.db


 # Helper tables to connect the tables in the DB
 # Connects users to the divisoins they are a part of
 # This connection is mainly to access which role a user has i a certain divsion
user_division = db.Table('user_division',
                           db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
                           db.Column('division_id', db.Integer,db.ForeignKey('division.id')),
                           db.Column('role',db.String(255))
)

# Connects users to the groups they are a part of
user_group = db.Table('user_group',
                        db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
                        db.Column('group_id',db.Integer,db.ForeignKey('groups.id'))
)

# Connects divsions to parameter
division_parameter = db.Table('division_parameter',
                                db.Column('division_id', db.Integer, db.ForeignKey('division.id')),
                                db.Column('parameter_id', db.Integer, db.ForeignKey('parameter.id'))
                                )

# Connects parameter to value, probably is unnecessary seeing as the next table will do the same job
parameter_value = db.Table('parameter_value',
                            db.Column('parameter_id',db.Integer,db.ForeignKey('parameter.id')),
                            db.Column('value_id',db.Integer,db.ForeignKey('value.id'))
)

# connects users, division, parameter and value
user_division_parameter_value = db.Table('user_division_parameter_value',
                                             db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
                                             db.Column('division_id',db.Integer,db.ForeignKey('division.id')),
                                             db.Column('parameter_id',db.Integer,db.ForeignKey('parameter.id')),
                                             db.Column('value_id',db.Integer, db.ForeignKey('value.id'))
)

#class UserDivision(db.Model):
#
#    __tablename__ = "user_division"
#
#    division_id = db.Column(db.Integer, primary_key = True)
#    user_id = db.Column(db.Integer, primary_key = True)
#    role = db.Column(db.String(255))
#
#    def __repr__(self):
#        return "DivisionID: " + str(self.division_id) + " UserID: " + str(self.user_id) + " Role: " + str(self.role)
#
class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), unique = False)
    lastname = db.Column(db.String(255), unique = False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique =False)
    divisions_created = db.relationship("Division", backref='creators')
    divisions = db.relationship('Division', secondary=user_division, backref=db.backref('users', lazy='dynamic'))
    groups = db.relationship('Group',secondary=user_group, backref=db.backref('users', lazy='dynamic'))
    parameters = db.relationship('Parameter', secondary=user_division_parameter_value, backref=db.backref('users',lazy='dynamic'))
    values = db.relationship('Value', secondary=user_division_parameter_value, backref = db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return "ID: " + str(self.id) + ", name: " + str(self.firstname)+str(self.lastname)+ ", Email: " + str(self.email)

class Division(db.Model):
    __tablename__="division"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    groups = db.relationship('Group',backref='division')
    #users = db.relationship('User', secondary=user_division, backref=db.backref('division', lazy='dynamic'))
    parameters = db.relationship('Parameter', secondary=division_parameter,  backref=db.backref('division', lazy='dynamic'))



    def __repr__(self):
        return "ID: " + str(self.id) + ", name: " + str(self.name)+ ", creator: " + str(self.creator_id)


"""
class User_Division(db.Model):
    __tablename__="user_division"
    userID = db.Column(db.Integer, primary_key=True)
    divisionID = db.Column(db.Integer,primary_key=True)
    role = db.Column(db.String(255))
    def __repr__(self):
        return "userID: " + str(self.userID) + ", divisionID: " + str(self.divisionID) + ", users role: " + str(self.role)
"""


class Group(db.Model):
    __tablename__="groups"
    id = db.Column(db.Integer, primary_key=True)
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'))
    leader_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #members = db.relationship('User', secondary=user_group, backref=db.backref('groups',lazy='dynamic'))

    def __repr__(self):
        return "ID: " + str(self.id) + ", divisionID: " + str(self.division_id) + ", leader: " + str(self.leader_id)

"""
class User_Group(db.Model):
    __tablename__="user_group"
    userID = db.Column(db.Integer,primary_key=True)
    groupID = db.Column(db.Integer,primary_key=True)
    def __repr__(self):
        return "userID: " + str(self.userID) + ", groupID: " + str(self.groupID)
"""

class Parameter(db.Model):
    __tablename__="parameter"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    values = db.relationship('Value', secondary=parameter_value, backref=db.backref('parameter',lazy='dynamic'))
    # users = db.relationship('User', secondary=user_division_parameter_value, backref=db.backref('parameter', lazy='dynamic'))
    # divisions = db.relationship('Division', secondary=user_division_parameter_value, backref=db.backref('parameter',lazy='dynamic'))

    number_param = db.relationship('NumberParam', back_populates="parameter", uselist=False) # One-to-One
    enum_variants = db.relationship('EnumVariant', back_populates="parameter") #One-to-Many

    def __repr__(self):
        return "ID: " + str(self.id) + ", description: " + str(self.description)

class NumberParam(db.Model):
    __tablename__="number_param"
    min = db.Column(db.Integer)
    max = db.Column(db.Integer)
    parameter_id = db.Column(db.Integer, db.ForeignKey('parameter.id'), primary_key=True)

    parameter = db.relationship('Parameter', back_populates="number_param")

    def __repr__(self):
        return "min: " + str(self.min) + ", max: " + str(self.max) + ", parameter_id: " + str(self.parameter_id)

class EnumVariant(db.Model):
    __tablename__="enum_variant"
    name = db.Column(db.String(50), primary_key=True)
    parameter_id = db.Column(db.Integer, db.ForeignKey('parameter.id'), primary_key=True)

    parameter = db.relationship('Parameter', back_populates="enum_variants")



class Value(db.Model):
    __tablename__="value"
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    description = db.Column(db.String(255))
    # parameters = db.relationship('Parameter', secondary=parameter_value, backref=db.backref('value',lazy='dynamic'))
    # users = db.relationship('User', secondary=user_division_parameter_value, backref=db.backref('value', lazy='dynamic'))
    # divisions = db.relationship('Division', secondary=user_division_parameter_value, backref=db.backref('value', lazy='dynamic'))

    def __repr__(self):
        return "ID: " + str(self.id) + ", description: " + str(self.description)

"""
class Parameter_Value(db.Model):
    __tablename__ = "parameter_value"
    parameterID = db.Column(db.Integer, primary_key=True)
    valueID = db.Column(db.Integer, primary_key=True)
    def __repr__(self):
        return "parameterID: " + str(self.parameterID) + ", valueID: " + str(self.valueID)
"""

"""
class User_Division_Parameter_Value(db.Model):
    __tablename__ = "user_division_parameter_value"
    userID = db.Column(db.Integer, primary_key=True)
    divisionID = db.Column(db.Integer, primary_key=True)
    parameterID = db.Column(db.Integer, primary_key=True)
    valueID = db.Column(db.Integer, primary_key=True)
    def __repr__(self):
        return "userID: " + str(self.parameterID) + ", divisionID: " + str(self.valueID) +\
               "parameterID: " + str(self.parameterID) + ", valueID: " + str(self.valueID)
"""
