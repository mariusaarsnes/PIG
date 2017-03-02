
class get_divisions:

    def __init__(self, database, User):
        self.database = database
        self.User = User

    def fetch_divisions(self, current_user):

        divisions_participating = self.database.get_session().query(self.User).filter(self.User.id==current_user.id).first().divisions
        divisions_created = self.database.get_session().query(self.User).filter(self.User.id ==current_user.id).first().divisions_created
        return divisions_participating, divisions_created




