# encoding=UTF-8

class DivideGroupsToLeaders:

    def __init__(self,database, Division, user_division, db_getters):
        self.database = database
        self.Division = Division
        self.user_division = user_division
        self.db_getters = db_getters

    # TODO: Only used in tests
    def assign_leaders_to_groups(self,current_user,division_id):
        leaders = self.db_getters.get_all_leaders_in_division(current_user,division_id)
        groups = self.db_getters.get_all_groups_in_division(current_user,division_id)

        counter = 0
        for group in groups:
            group.leader_id = leaders[counter].id
            counter +=1
            if counter == len(leaders):
                counter = 0
        self.database.get_session().commit()
        return




