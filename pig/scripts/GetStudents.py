# encoding=UTF-8

class GetStudents:

    print("print a calss")

    def __init__(self,database, Division, user_division):
        self.database = database
        self.Division = Division
        self.user_division = user_division

    def get_all_students(self, current_user, division_id):
        students = self.database.get_session().query(self.user_division)\
            .filter(self.user_division._columns.get('division_id')== division_id,
                    self.user_division._columns.get('role')=='Member').first()
        return students
        



    
    




