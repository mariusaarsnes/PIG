__author__ = 'owner_000'

class User:

    def __init__(self, username, password, id):
        self.username = username
        self.passowrd = password
        self.id = id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.id

