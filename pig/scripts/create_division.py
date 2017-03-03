from sqlalchemy import func
import sys

class create_division:

    def __init__(self, database, Division, Parameter):
        self.database = database
        self.Parameter = Parameter
        self.Division = Division
        self.parameters = {};

    def register_division(self, current_user, form):
        print('Registering division...', file=sys.stderr)
        division = self.Division(name = form["Division"], creator_id = current_user.id)
        for key in form:
            print('form[%s] = %s' % (key, form[key]), file=sys.stderr)
            if key == "Division":
                pass
            elif key.startswith("Parameter"):
                param_nr = int(key[9])
                print(' - Parameter of %s' % param_nr, file=sys.stderr)
                # Old code start - Creates a new Parameter row
                parameter = self.database.get_session().query(self.Parameter).filter(form[key].strip().lower() == func.lower(self.Parameter.description)).first()
                if parameter is None:
                    parameter = self.Parameter(description=form[key].strip())
                division.parameters.append(parameter)
                # Old code end
            elif key.startswith("Type"):
                param_nr = int(key[4])
                print(' - Type of %s' % param_nr, file=sys.stderr)
                pass
            elif key.startswith("Min"):
                param_nr = int(key[3])
                print(' - Min of %s' % param_nr, file=sys.stderr)
                pass
            elif key.startswith("Max"):
                param_nr = int(key[3])
                print(' - Max of %s' % param_nr, file=sys.stderr)
                pass
            elif key.startswith("Option"):
                param_nr = int(key[6])
                print(' - Option of %s' % param_nr, file=sys.stderr)
                pass

        self.database.get_session().add(division)
        self.database.get_session().commit()




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
