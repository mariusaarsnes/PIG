import pig.scripts.encryption as e

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
        divisions_participating = self.database.get_session()\
            .query(self.user_division, self.Division, self.User)\
            .filter(self.user_division._columns.get("user_id") == current_user.id,
                    self.Division.id == self.user_division._columns.get("division_id"),
                    self.User.id == self.Division.creator_id).all()

        divisions_created = self.database.get_session().query(self.User)\
            .filter(self.User.id ==current_user.id)\
            .first()\
            .divisions_created
        ta_links, student_links  = [], []
        for division in divisions_created:
            ta_links.append(self.get_link(key, division.name, division.id, 1))
            student_links.append(self.get_link(key, division.name, division.id, 0))
        return divisions_participating, divisions_created, ta_links, student_links

    def get_link(self, key, division_name, division_id, leader):
        return "apply_group?values=" + e.encode(key, division_name+"," + str(division_id) + "," + str(leader))

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

    #This returns a dict with users as key, and all of their answered parameters (values as a list) as value
    def get_all_users_with_values(self, division_id):
        list = self.database.get_session()\
                .query(self.User, self.Value)\
                .filter(self.Value.id == self.user_division_parameter_value._columns.get("value_id"),\
                         self.User.id == self.user_division_parameter_value._columns.get("user_id"),\
                         division_id == self.user_division_parameter_value._columns.get("division_id"))\
                 .all()
        user_list = {}
        for val in list:
            if val[0] not in user_list:
                user_list.update({val[0]:[]})
            for value in val[1:]:
                user_list[val[0]].append(value)
        return user_list

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
            print("ERROR: No leaders signed up for division ",division_id)
            return None
        return leaders

    def get_groups(self, division_id):
        division = self.database.get_session().query(self.Division).filter(self.Division.id == division_id).first()
        return division.groups if division is not None else []

    def get_groupless_users(self, division_id):
        # Get users that are in some group in some division
        subquery = self.database.get_session().query(self.User.id).filter(
                                self.Group.id == self.user_group._columns.get("group_id"),
                                division_id == self.Group.division_id,
                                self.user_group._columns.get("user_id") == self.User.id).all()
        # Get users signed up as member for that division (by user_division), that are not in a group
        return self.database.get_session().query(self.User).filter(
                                self.user_division._columns.get("division_id") == division_id,
                                self.user_division._columns.get("user_id") == self.User.id,
                                self.user_division._columns.get("role") == "Member",
                                ~self.User.id.in_(subquery)).all()

    def is_registered_to_division(self, user_id, division_id):
        user_div = self.database.get_session().query(self.user_division)\
                .filter(self.user_division._columns.get("user_id") == user_id,\
                    self.user_division._columns.get("division_id") == division_id)\
                .first()
        return user_div is not None

    def get_all_students(self, current_user, division_id):
        students = self.database.get_session().query(self.User)\
            .filter(self.user_division._columns.get('division_id')== division_id,
                    self.user_division._columns.get('user_id') == self.User.id,
                    self.user_division._columns.get('role')=='Member').all()
        return students
