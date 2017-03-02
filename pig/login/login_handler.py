from pig.login.user import user as LoginUser

class login_handler:

    def __init__(self, database, User):
        self.database = database
        self.User = User

    def get_user_with_id(self, id):
        user = self.database.get_session().query(self.User).filter(self.User.id == id).first()
        return self.get_user(user.email, user.password)

    def get_user(self, email, password):
        user = self.database.get_session().query(self.User).filter(self.User.password == password, self.User.email == email).first()
        if user is not None:
            return LoginUser(email, password, user.firstname + " " + user.lastname, user.id)
        return None