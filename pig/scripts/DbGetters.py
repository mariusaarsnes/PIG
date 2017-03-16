class DbGetters:
    def __init__(self,database, User, Division, Group, Parameter, Value, NumberParam, EnumVariant,
                 user_division, user_group, division_parameter,parameter_value ,user_division_parameter_value):
        self.database = database
        self.User = User
        self.Division = Division
        self.Group = Group
        self.Paramter = Parameter
        self.Value = Value
        self.NumberParam = NumberParam
        self.EnumVariant = EnumVariant

        self.user_division = user_division
        self.user_division = user_group
        self.division_parameter = division_parameter
        self.parameter_value = parameter_value
        self.user_division_parameter_value = user_division_parameter_value

    def