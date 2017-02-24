from pig.app import db


class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), unique = False)
    lastname = db.Column(db.String(255), unique = False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique =False)
    divisions = db.relationship("Division", backref='users', lazy='dynamic')

    def __repr__(self):
        return "ID: " + str(self.id) + ", name: " + str(self.firstname)+str(self.lastname)+ ", Email: " + str(self.email)

class Division(db.Model):
    __tablename__="divisions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    creatorID = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __repr__(self):
        return "ID: " + str(self.id) + ", name: " + str(self.name)+ ", creator: " + str(self.creatorID)

users_divisions = db.Table('users_divisions',
                           db.Column('userID',db.Integer,db.ForeignKey('users.id')),
                           db.Column('divisionID', db.Integer,db.ForeignKey('divisions.id'))
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
    divisionID = db.Column(db.Integer, primary_key=True, )
    leaderID = db.Column(db.Integer)

    def __repr__(self):
        return "ID: " + str(self.id) + ", divisionID: " + str(self.divisionID) + ", leader: " + str(self.leaderID)


class User_Group(db.Model):
    __tablename__="users_groups"
    userID = db.Column(db.Integer,primary_key=True)
    groupID = db.Column(db.Integer,primary_key=True)

    def __repr__(self):
        return "userID: " + str(self.userID) + ", groupID: " + str(self.groupID)


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
        return "ID: " + str(self.id) + ", description: " + str(self.divisionID) + ", value: " + str(self.value)

class Parameter_Value(db.Model):
    __tablename__ = "parameters_values"
    parameterID = db.Column(db.Integer, primary_key=True)
    valueID = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "parameterID: " + str(self.parameterID) + ", valueID: " + str(self.valueID)

class User_Division_Parameter_Value(db.Model):
    __tablename__ = "users_divisions_parameters_values"
    userID = db.Column(db.Integer, primary_key=True)
    divisionID = db.Column(db.Integer, primary_key=True)
    parameterID = db.Column(db.Integer, primary_key=True)
    valueID = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "userID: " + str(self.parameterID) + ", divisionID: " + str(self.valueID) +\
               "parameterID: " + str(self.parameterID) + ", valueID: " + str(self.valueID)




