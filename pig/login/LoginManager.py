__author__ = 'owner_000'
from pig.login.User import User

class LoginManager:

    def __init__(self):
        pass

    users = {
            "daniel": ("test", 0),
            "marius": ("passord", 1)
            }

    @classmethod
    def get_user_with_id(self, id):
        for k in self.users:
            if self.users[k][1] == id:
                return self.get_user(k, self.users[k][0])
        return None

    @classmethod
    def get_user(self, username, password):
        if username in self.users and self.users[username][0] == password:
            return User(username, password, self.users[username][1])
        return None