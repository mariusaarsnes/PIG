
class DivideLeaders:

    def __init__(self, database, User, Division):
        self.database = database
        self.User = User
        self.Division = Division

    def assign_leaders(self, division_id):
        print(self.database.get_session().execute("SELECT * FROM user_divison WHERE division_id = " + str(division_id) + "  AND role = 'Student'").all())
        pass