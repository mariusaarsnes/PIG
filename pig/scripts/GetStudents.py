# encoding=UTF-8

class GetStudents:

    print("On GetStudents")

    def __init__(self,database, Division, user_division, User):
        self.User = User
        self.database = database
        self.Division = Division
        self.user_division = user_division

    def get_all_students(self, current_user, division_id):
        students = self.database.get_session().query(self.User)\
            .filter(self.user_division._columns.get('division_id')== division_id,
                    self.user_division._columns.get('user_id') == self.User.id,
                    self.user_division._columns.get('role')=='Member').all()
        return students
        

    def get_all_divisions_where_creator_for_given_user(self,current_user):
        return self.database.get_session().query(self.User)\
            .filter(self.User.id == current_user.id).first().divisions_created

    
    




