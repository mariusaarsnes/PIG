# encoding=UTF-8

class GetStudents:

    print("print a calss")

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
        



    
    




