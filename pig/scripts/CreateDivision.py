
class CreateDivision:

    def __init__(self, database, Division, Parameter):
        self.database = database
        self.Parameter = Parameter
        self.Division = Division

    def register_division(self, current_user, form):
        division = self.Division(name = form["Division"], creator_id = current_user.id)
        for key in form:
            if not key == "Division":
                parameter = self.Parameter(description=form[key])
                division.parameters.append(parameter)
        self.database.get_session().add(division)
        self.database.get_session().commit()