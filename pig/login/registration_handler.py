class registration_handler:

    def __init__(self, database, User):
        self.database = database
        self.User = User

    def create_user(self, firstname, lastname, email, password):
        user = self.User(firstname=firstname, lastname=lastname, email=email, password=password)
        self.database.get_session().add(user)
        self.database.get_session().commit()

    def validate_form(self, form):
        for k in form:
            if form[k] is "":
                return False, "Please make sure all of the fields are filled."
        if not form["Password"] == form["PasswordConfirm"]:
            return False, "The passwords does not match."
        elif not self.validate_email(form["Email"]):
            return False, "The entered email was invalid."
        return True, None

    def validate_email(cls, email):
        split = email.split("@")
        return len(split) == 2 and "." in split[1]