from re import match

class RegistrationHandler:

    email_regex = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

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
        elif not match(self.email_regex, form["Email"]) or "." not in form["Email"].split("@")[1]:
            return False, "The entered email was invalid."
        user = self.database.get_session().query(self.User).filter(self.User.email == form["Email"]).first()
        if not user is None:
            return False, "A user with that email already exist."
        return True, None
