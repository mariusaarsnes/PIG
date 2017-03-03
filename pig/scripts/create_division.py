from sqlalchemy import func

class create_division:

    def __init__(self, database, Division, Parameter):
        self.database = database
        self.Parameter = Parameter
        self.Division = Division

    def register_division(self, current_user, form):
        division = self.Division(name = form["Division"], creator_id = current_user.id)
        for key in form:
            if not key == "Division":
                parameter = self.database.get_session().query(self.Parameter).filter(form[key].strip().lower() == func.lower(self.Parameter.description)).first()
                if parameter is None:
                    parameter = self.Parameter(description=form[key].strip())
                division.parameters.append(parameter)
        self.database.get_session().add(division)
        self.database.get_session().commit()

