import pig.scripts.encryption as e

class get_divisions:

    def __init__(self, database, User):
        self.database = database
        self.User = User

    def fetch_divisions(self, current_user, key):
        divisions_participating = self.database.get_session().query(self.User).filter(self.User.id==current_user.id).first().divisions
        divisions_created = self.database.get_session().query(self.User).filter(self.User.id ==current_user.id).first().divisions_created
        ta_links, student_links  = [], []
        for division in divisions_created:
            ta_links.append("apply_group?values=" + e.encode(key, division.name+"," + str(division.id) + ",1"))
            student_links.append("apply_group?values=" + e.encode(key, division.name+"," + str(division.id) + ",0"))
        return divisions_participating, divisions_created, ta_links, student_links