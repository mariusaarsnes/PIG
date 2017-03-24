import pig.scripts.encryption as e
from re import match



class Tasks:
    email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

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

    def generate_links(self, key, divisions_created):
        ta_links, student_links = [], []
        for division in divisions_created:
            ta_links.append(self.get_link(key, division.name, division.id, 1))
            student_links.append(self.get_link(key, division.name, division.id, 0))
        return ta_links, student_links

    @classmethod
    def get_link(self, key, division_name, division_id, leader):
        return "apply_group?values=" + e.encode(key, division_name + "," + str(division_id) + "," + str(leader))



    def register_user_for_division_for_given_division_id_and_role(self, current_user, division_id, role):
        division = self.database.get_session() \
                .query(self.Division) \
                .filter(self.Division.id == division_id) \
                .first()
        division.users.append(current_user)

        self.database.get_session().commit()