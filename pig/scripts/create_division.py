from sqlalchemy import func
import sys

class create_division:

    def __init__(self, database, Division, Parameter, NumberParam):
        self.database = database
        self.Division = Division
        self.Parameter = Parameter
        self.NumberParam = NumberParam
        self.parameters = {} # int -> Parameter
        self.specializations = {} # int -> NumberParam or EnumParam

    def register_division(self, current_user, form):
        print('Registering division...', file=sys.stderr)
        print('Input: %s' % form, file=sys.stderr)
        division = self.Division(name = form["Division"], creator_id = current_user.id)

        # First pass: Find the type of each parameter
        for (key, value) in form.items():
            if key == "Division":
                pass

            elif key.startswith("Parameter"):
                param_nr = int(key[9])

                parameter = self.database.get_session() \
                    .query(self.Parameter) \
                    .filter(value.strip().lower() == func.lower(self.Parameter.description)) \
                    .first()

                if parameter is None:
                    # Create new Parameter only if it does not exist
                    parameter = self.Parameter(description=value.strip())
                    print("Create parameter with ID = %s" % parameter.id, file=sys.stderr)
                    self.database.get_session().add(parameter)
                    self.parameters[param_nr] = parameter
                else:
                    # Parameter already exists - Don't create it, just add it to the Division
                    # Setting it to None here signifies for later that we should not add a specialization for it
                    self.parameters[param_nr] = None
                    pass

                division.parameters.append(parameter)

                self.specializations[param_nr] = None

            elif key.startswith("Type"):
                param_nr = int(key[4])
                if value == "Number":
                    self.specializations[param_nr] = self.NumberParam(min=None, max=None)
                else:
                    print("Haven't implemented enum yet", file=sys.stderr)
                    exit(1)

        # Second pass: Find the configurations for each parameters
        for (key, value) in form.items():

            if key.startswith("Min"):
                param_nr = int(key[3])
                if isinstance(self.specializations[param_nr], self.NumberParam):
                    print("Min: Parameter is Number", file=sys.stderr)
                    self.specializations[param_nr].min = int(value)
                else:
                    print("Min: Parameter is not Number.. %s" % self.specializations[param_nr], file=sys.stderr)
                    pass

            elif key.startswith("Max"):
                param_nr = int(key[3])
                if isinstance(self.specializations[param_nr], self.NumberParam):
                    self.specializations[param_nr].max = int(value)
                else:
                    pass

            elif key.startswith("Option"):
                param_nr = int(key[6])
                # TODO

        # Commit the new Parameters so that they get assigned primary keys - these will be used in the next pass
        self.database.get_session().commit()

        # For every parameter, add it and its specialization to the database
        for param_nr in self.specializations.keys():
            param = self.parameters[param_nr]
            spec = self.specializations[param_nr]
            # `param is None` signifies that the parameter was already in the Database, and that we should not
            # make another specialization
            if not param is None:
                print("Param ID = %s" % param.id, file=sys.stderr)
                spec.parameter = param
                self.database.get_session().add(spec)

        self.database.get_session().add(division)
        self.database.get_session().commit()

    def make_parameter(self, desc):
        parameter = self.database.get_session() \
            .query(self.Parameter) \
            .filter(desc.strip().lower() == func.lower(self.Parameter.description)) \
            .first()
        if parameter is None:
            parameter = self.Parameter(description=desc.strip())
        return parameter;


# Example for reference


#  form[Division] = navn
#  form[Parameter1] = en
#  form[Type1] = Enum
#  form[Min1] = 
#  form[Max1] = 
#  form[Option1_1] = a
#  form[Option1_2] = b
#  form[Option1_3] = c
#  form[Parameter2] = nu
#  form[Type2] = Number
#  form[Min2] = 0
#  form[Max2] = 10
