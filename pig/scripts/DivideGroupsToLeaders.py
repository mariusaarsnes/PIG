# encoding=UTF-8

class DivideGroupsToLeaders:

    def __init__(self,database, Division, user_division):
        self.database = database
        self.Division = Division
        self.user_division = user_division


    def fetch_groups(self,current_user,division_id):
        groups = self.database.get_session().query(self.Division)\
            .filter(self.Division.creator_id == current_user.id, self.Division.id == division_id).first()
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
        print("current user: " + str(current_user))
        print("division id:" + str(division_id))
        leaders, groups = self.fetch_groups(current_user,division_id)

        groups_per_leader = len(groups)//len(leaders)
        counter = 0
        for group in groups:
            group.leader_id = leaders[counter].user_id
            counter +=1
            if (counter == groups_per_leader):
                counter = 0
        self.database.get_session().commit()




