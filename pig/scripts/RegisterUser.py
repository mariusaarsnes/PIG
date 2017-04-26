__author__ = 'owner_000'

class RegisterUser():

    def __init__(self, database, User, Division, user_division, Value, Parameter):
        self.database = database
        self.Parameter = Parameter
        self.User = User
        self.Value = Value
        self.Division = Division
        self.user_division = user_division

    #Registers a user for a given division
    def register_user(self, current_user, division_id, role):
        try:
            self.database.get_session().execute("INSERT INTO user_division VALUES(:user_id, :division_id, :role)", {"user_id": current_user.id, "division_id": int(division_id), "role": role})
            self.database.get_session().commit()
        except Exception:
            pass
            #The user is already registered.

    #Registers the parameters a user typed into the signup form
    def register_parameters(self, current_user, form):
        divisionId = int(form["DivisionId"])
        for (key, value) in form.items():
            if key.startswith("Parameter"):
                id = key[9:]
                value_parameter = self.database.get_session().query(self.Value).filter(self.Value.value == value).first()
                if value_parameter is None:
                    value_parameter = self.Value(value=value)
                    self.database.get_session().add(value_parameter)
                    self.database.get_session().commit()
                    value_parameter = self.database.get_session().query(self.Value).filter(self.Value.value == value).first()
                parameter = self.database.get_session().query(self.Parameter).filter(self.Parameter.id == id).first()
                self.database.get_session().execute("INSERT INTO user_division_parameter_value VALUES(:user_id, :division_id, :parameter_id, :value_id)",
                            {"user_id": current_user.id, "division_id": divisionId, "parameter_id": parameter.id, "value_id": value_parameter.id})
        self.database.get_session().commit()

    #Checks if the user is the creator of the specified division
    def is_division_creator(self, current_user, division_id):
        return self.database.get_session().query(self.Division).filter(self.Division.id == division_id, self.Division.creator_id == current_user.id).first() is not None
