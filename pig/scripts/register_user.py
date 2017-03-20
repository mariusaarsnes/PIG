__author__ = 'owner_000'

class Task_RegisterUser():

    def __init__(self, database, User, Division, user_division):
        self.database = database
        self.User = User
        self.Division = Division
        self.user_division = user_division

    def register_user(self, current_user, division_id, role):
        #  self.database.get_session().execute("INSERT INTO user_division VALUES(:user_id, :division_id, :role)", {"user_id": current_user.id, "division_id": int(division_id), "role": role})
        division = self.database.get_session() \
                .query(Division) \
                .filter(Division.id == division_id) \
                .first()
        division.users.append(current_user)

        self.database.get_session().commit()
