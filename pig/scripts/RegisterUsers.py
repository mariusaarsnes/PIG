__author__ = 'owner_000'

class RegisterUser():

    def __init__(self, database, User, Division, user_division):
        self.database = database
        self.User = User
        self.Division = Division
        self.user_division = user_division

    def register_user(self, current_user, division_id, role):
        #user = self.database.get_session().query(self.User).filter(self.User.id == current_user.id).first()
        #division = self.database.get_session().query(self.Division).filter(self.Division.id == division_id).first()
        #user.divisions.append(division)
        #self.database.get_session().add(self.user_division(division_id = division_id, user_id = current_user.id, role = role))
        div = self.user_division(user_id = current_user.id, division_id = division_id, role = role)
        self.database.get_session().add(div)
        self.database.get_session().commit()
