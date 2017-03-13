class GetGroups:

    def __init__(self,database, User, Group):
        self.database = database
        self.User = User
        self.Group = Group

    def get_groups_leading(self,current_user):
        return self.database.get_session().query(self.Group).filter(self.Group.leader_id == current_user.id).all()
