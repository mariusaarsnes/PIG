__author__ = 'owner_000'

class UserScripts:

    def __init__(self, database, User, Division, user_division, user_group, Group):
        self.database = database
        self.User = User
        self.Division = Division
        self.user_division = user_division
        self.user_group = user_group
        self.Group = Group

    def get_groups(self, group_id):
        values = self.database.get_session().query(self.Division).filter(self.Division.id == group_id).first().groups
        return values

    def get_groupless_users(self, division_id):
        subquery = self.database.get_session().query(self.User.id).filter(self.Group.id == self.user_group._columns.get("group_id"),\
                                    self.Division.id == self.Group.division_id,\
                                    self.user_group._columns.get("user_id") == self.User.id).all()

        return self.database.get_session().query(self.User).filter(self.user_division._columns.get("division_id") == division_id,\
                                                                                    self.user_division._columns.get("user_id") == self.User.id,\
                                                                                    ~self.User.id.in_(subquery)).all()
