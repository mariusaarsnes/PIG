__author__ = 'owner_000'

class RegisterUser():

    def __init__(self, database, User, Division, user_division):
        self.database = database
        self.User = User
        self.Division = Division
        self.user_division = user_division

    def register_user(self, current_user, division_id, role):
        self.database.get_session().execute("INSERT INTO user_division VALUES(:user_id, :division_id, :role)", {"user_id": current_user.id, "division_id": int(division_id), "role": role})
        self.database.get_session().commit()

    def is_group_leader(self, current_user, division_id):
        return self.database.get_session().query(self.Division).filter(self.Division.id == division_id, self.Division.creator_id == current_user.id).first() is not None