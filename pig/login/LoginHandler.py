from pig.login.User import User as LoginUser
from passlib.hash import bcrypt

#Class that handles the login process
class LoginHandler:

    def __init__(self, database, User):
        self.database = database
        self.User = User

    #Gets a user instance based on the user id
    def get_user_with_id(self, id):
        user = self.database.get_session().query(self.User).filter(self.User.id == id).first()
        if user is None:
            return None
        return self.get_user(user.email, user.password)

    #Queries the database for a user with the provided email & password, then crates a new user object with database data
    def get_user(self, email, password):
        user = self.database.get_session().query(self.User).filter(self.User.email == email).first()
        if user is not None:
            try:
                if bcrypt.verify(password, user.password) or password == user.password:
                    return LoginUser(email, password, user.firstname + " " + user.lastname, user.id)
            except:
                print("Password in the database is not hashed")
        return None