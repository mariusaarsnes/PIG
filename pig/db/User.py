from pig.app import db

class User(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return "User: " + str(self.id) + ", Email: " + str(self.email)