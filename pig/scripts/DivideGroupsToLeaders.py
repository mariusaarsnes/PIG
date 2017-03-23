# encoding=UTF-8

class DivideGroupsToLeaders:

    def __init__(self,database, Division, user_division, db_getters):
        self.database = database
        self.Division = Division
        self.user_division = user_division
        self.db_getters = db_getters


    def fetch_groups(self,current_user,division_id):
        groups = self.database.get_session().query(self.Division)\
            .filter(self.Division.creator_id == current_user.id, self.Division.id == division_id).first()
        print(groups)
        if (groups is None):
            print("ERROR: No groups in division ", division_id)
            return

        leaders = self.database.get_session().query(self.user_division)\
            .filter(self.user_division._columns.get('division_id')== division_id,
                    self.user_division._columns.get('role')=='Leader').all()
        if (leaders is None):
            print("ERROR: No leaders signed up for divisions ", division_id)
            return

        groups = groups.groups
        leaders = leaders
        return leaders, groups

    def assign_leaders_to_groups(self,current_user,division_id):
        leaders = self.db_getters.get_all_leaders_in_division_for_given_creator_and_division_id(current_user,division_id)
        groups = self.db_getters.get_all_groups_in_division_for_given_creator_and_division_id(current_user,division_id)

        counter = 0
        for group in groups:
            group.leader_id = leaders[counter].id
            counter +=1
            if counter == len(leaders):
                counter = 0
        self.database.get_session().commit()
        return




