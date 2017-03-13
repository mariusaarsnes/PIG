import pig.scripts.encryption as e

class Task_GetDivisions:

    def __init__(self, database, User,Group):
        self.database = database
        self.User = User
        self.Group = Group
    #Fetches the divisions related to the user and creates signup links for the divisions
    def fetch_divisions(self, current_user, key):
        divisions_participating = self.database.get_session().query(self.User).filter(self.User.id==current_user.id).first().divisions
        divisions_created = self.database.get_session().query(self.User).filter(self.User.id ==current_user.id).first().divisions_created
        ta_links, student_links  = [], []
        for division in divisions_created:
            ta_links.append(self.get_link(key, division.name, division.id, 1))
            student_links.append(self.get_link(key, division.name, division.id, 0))
        return divisions_participating, divisions_created, ta_links, student_links

    @classmethod
    def get_link(self, key, division_name, division_id, leader):
        return "apply_group?values=" + e.encode(key, division_name+"," + str(division_id) + "," + str(leader))
