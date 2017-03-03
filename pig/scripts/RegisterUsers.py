__author__ = 'owner_000'
from sqlalchemy.sql import text

class RegisterUser():

    def __init__(self, database, User, Division, user_division):
        self.database = database
        self.User = User
        self.Division = Division
        self.user_division = user_division

    def register_user(self, current_user, division_id, role):
        self.database.get_session().execute("INSERT INTO user_division VALUES(:user_id, :division_id, :role)", {"user_id": current_user.id, "division_id": int(division_id), "role": role})
        self.database.get_session().commit()
