import pig.scripts.encryption as e

class Task_GetDivisions:

    def __init__(self, database, User, Division, user_division):
        self.database = database
        self.Division = Division
        self.user_division = user_division
        self.User = User
    #Fetches the divisions related to the user and creates signup links for the divisions

    @classmethod
    def get_link(self, key, division_name, division_id, leader):
        return "apply_group?values=" + e.encode(key, division_name+"," + str(division_id) + "," + str(leader))
