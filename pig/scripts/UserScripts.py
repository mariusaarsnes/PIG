__author__ = 'owner_000'

class UserScripts:

    def __init__(self, database, User, Division, user_division):
        self.database = database
        self.User = User
        self.Division = Division
        self.user_division = user_division

    def get_groups(self, group_id):
        values = self.database.get_session().query(self.Division).filter(self.Division.id == group_id).first().groups
        return values

    def get_groupless_users(self, group_id):
        self.database.query(self.User, self.user_division, self.Division).filter(self.User)
