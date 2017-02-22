from app import db

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(64),
                          index=True,unique=False)
    lastName = db.Column(db.String(64),
                         index=True, unique=False)
    
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.String(64), index=True, uniqeu= False)

    def __repr__(self):
        return '<User %r %r>' % (self.firstName, self.lastName)