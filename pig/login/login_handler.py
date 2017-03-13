from pig.login.user import user as LoginUser

#Class that handles the login process
class LoginHandler:

    def __init__(self, database, User):
        self.database = database
        self.User = User

    #Gets a user instance based on the user id
    def get_user_with_id(self, id):
        user = self.database.get_session().query(self.User).filter(self.User.id == id).first()
        return self.get_user(user.email, user.password)

    #Queries the database for a user with the provided email & password, then crates a new user object with database data
    def get_user(self, email, password):
        user = self.database.get_session().query(self.User).filter(self.User.password == password, self.User.email == email).first()
        if user is not None:
            return LoginUser(email, password, user.firstname + " " + user.lastname, user.id)
        return None
