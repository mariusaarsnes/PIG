class DbGetters:
    def __init__(self,database, User, Division, Group, Parameter, Value, NumberParam, EnumVariant,
                 user_division, user_group, division_parameter,parameter_value ,user_division_parameter_value):
        self.database = database
        self.User = User
        self.Division = Division
        self.Group = Group
        self.Parameter = Parameter
        self.Value = Value
        self.NumberParam = NumberParam
        self.EnumVariant = EnumVariant

        self.user_division = user_division
        self.user_group = user_group
        self.division_parameter = division_parameter
        self.parameter_value = parameter_value
        self.user_division_parameter_value = user_division_parameter_value
        return

    def get_all_divisions(self):
        return self.database.get_session().query(self.Division).all()

    def get_all_divisions_where_creator_for_given_user(self,current_user):
        return self.database.get_session().query(self.User)\
            .filter(self.User.id == current_user.id).first().divisions_created

    def fetch_divisions(self, current_user, key):
        divisions_participating = self.database.get_session().query(self.user_division, self.Division, self.User).filter(self.user_division._columns.get("user_id") == current_user.id, \
                                                                                                              self.Division.id == self.user_division._columns.get("division_id"),\
                                                                                                            self.User.id == self.Division.creator_id).all()
        divisions_created = self.database.get_session().query(self.User).filter(self.User.id ==current_user.id).first().divisions_created
        ta_links, student_links  = [], []
        for division in divisions_created:
            ta_links.append(self.get_link(key, division.name, division.id, 1))
            student_links.append(self.get_link(key, division.name, division.id, 0))
        return divisions_participating, divisions_created, ta_links, student_links

    def get_all_divisions_where_leader_for_given_user(self,current_user):

        divisions = self.database.get_session().query(self.Division)\
            .filter(self.user_division._columns.get('division_id') == self.Division.id)\
            .filter(self.user_division._columns.get('user_id') == current_user.id)\
            .filter(self.user_division._columns.get('role') == 'Leader')\
            .order_by(self.Division.id).all()

        if (len(divisions) <1):
            print("ERROR: No divisions where user is leader")
            return None
        else:
            return divisions

    def get_all_divisions_where_member_or_leader_for_given_user(self,current_user):
        return self.database.get_session().query(self.user_division, self.Division, self.User).filter(self.user_division._columns.get("user_id") == current_user.id, \
                                                                                                              self.Division.id == self.user_division._columns.get("division_id"),\
                                                                                                            self.User.id == self.Division.creator_id).all()

    def get_all_divisions_where_member_for_given_user(self,current_user):
        return self.database.get_session().query(self.Division)\
            .filter(self.user_division._columns.get('user_id') == current_user.id)\
            .filter(self.user_division._columns.get('role') == 'Member').all()

    def get_all_groups_in_division_for_given_creator_and_division_id(self, creator, division_id):
        division = self.database.get_session().query(self.Division) \
            .filter(self.Division.creator_id == creator.id, self.Division.id == division_id).first()
        if (division is None):
            print("ERROR: No created division with id: ", division_id, "created by ",creator.id)
            return None
        return division.groups

    def get_user_groups(self, division_id):
        return self.database.get_session().query(self.User, self.Group.number).filter(self.user_division._columns.get('user_id') == self.User.id, 
                    self.user_division._columns.get('division_id') == division_id,
                    self.user_group._columns.get('group_id') == self.Group.id,
                    self.user_group._columns.get('user_id') == self.User.id,
                    self.Group.division_id == division_id).all()
            


    def get_all_leaders_in_division_for_given_creator_and_division_id(self,creator,division_id):
        leaders = self.database.get_session().query(self.User)\
            .filter(self.User.id == self.user_division._columns.get('user_id'))\
            .filter(self.user_division._columns.get('division_id')==division_id)\
            .filter(self.user_division._columns.get('role')=='Leader').all()
        if (len(leaders) <1):
            print("ERROR_ No leaders signed up for division ",division_id)
            return None
        return leaders

    def get_groups(self, division_id):
        division = self.database.get_session().query(self.Division).filter(self.Division.id == division_id).first()
        return division.groups if division is not None else []

    def get_groupless_users(self, division_id):
        subquery = self.database.get_session().query(self.User.id).filter(
                                self.Group.id == self.user_group._columns.get("group_id"),
                                self.Division.id == self.Group.division_id,
                                self.user_group._columns.get("user_id") == self.User.id).all()
        return self.database.get_session().query(self.User).filter(
                                self.user_division._columns.get("division_id") == division_id,
                                self.user_division._columns.get("user_id") == self.User.id,
                                self.user_division._columns.get("role") == "Member",
                                ~self.User.id.in_(subquery)).all()
