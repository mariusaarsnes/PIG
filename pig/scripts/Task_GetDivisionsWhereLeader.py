class Task_GetDivisionsWhereLeader:

    def __init__(self,database, Division, user_division):
        self.database = database
        self.Division = Division
        self.user_division = user_division

    def get_divisions_where_leader(self,current_user):
        divisions_where_is_leader = self.database.get_session().query(self.Division) \
            .filter(self.user_division._columns.get('division_id') == self.Division.id) \
            .filter(self.user_division._columns.get('user_id') == current_user.id) \
            .filter(self.user_division._columns.get('role') == 'Leader') \
            .order_by(self.Division.id).all()

        if (len(divisions_where_is_leader)) == 0:
            print("ERROR: No divisions where user is leader")
            return None
        else:
            return divisions_where_is_leader


