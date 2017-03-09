import os, pig, unittest
from flask_sqlalchemy import SQLAlchemy
from pig.db.models import *

class PigTestCase(unittest.TestCase):

    def setUp(self):
        pig.app.config['TESTING'] = True
        self.app = pig.app.test_client()


    def login(self,username,password):
        return self.app.post("/login", data=dict(Username=username,Password=password),follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    # Testing connection to db
    # This is done by just fetching an entry in users
    def test_connect_to_db(self):
        data = None
        try:
            data = database.get_session().query(User).first()
        except Exception as e1:
            print(e1)
        finally:
            assert data is not None

    # Testing login and logout.
    # First check tests with valid username and password
    # Second check test with invalid username but a valid password
    # Thid check tests with valid username but but invalid password
    def test_login_logout(self):
        rv = self.login('example1@gmail.com', 'password')
        assert b'Example' in rv.data
        rv = self.logout()
        assert b'Example' not in rv.data

        rv = self.login('ugyldig', 'password')
        assert b'ugyldig' not in rv.data

        rv = self.login('example@gmail.com','fewfewfw')
        assert b'hello' not in rv.data

    def test_create_division(self):
        pass

    #A helper method that sends a post request to the register page containing all of the registration-info
    def register(self, email, password, password_confirm, first_name, last_name):
        return self.app.post("/register", data=dict(Email=email, Password=password, PasswordConfirm=password_confirm, FirstName=first_name, LastName=last_name))

    #Testing registration of a user with two different passwords
    def test_register_user_with_two_different_password_inputs(self):
        rv = self.register("asd@asd.com", "test", "test1", "tester", "testing")
        assert b'does not match.' in rv.data

    #Testing registration of a user with invalid email
    def test_register_user_with_invalid_email(self):
        rv = self.register("asd@asd", "test", "test", "tester", "testing")
        assert b'email was invalid.' in rv.data
        rv = self.register("asd@as@d", "test", "test", "tester", "testing")
        assert b'email was invalid.' in rv.data
        rv = self.register("as..d@asd", "test", "test", "tester", "testing")
        assert b'email was invalid.' in rv.data

    #Testing if it is possible to register a user with one ore more empty fields
    def test_register_user_with_one_or_more_empty_fields(self):
        rv = self.register("asd@asd.com", "", "test", "tester", "testing")
        assert b'fields are filled.' in rv.data
        rv = self.register("asd@asd.com", "test", "", "tester", "testing")
        assert b'fields are filled.' in rv.data
        rv = self.register("", "test", "test", "tester", "testing")
        assert b'fields are filled.' in rv.data
        rv = self.register("asd@asd.com", "test", "test", "", "testing")
        assert b'fields are filled.' in rv.data
        rv = self.register("asd@asd.com", "test", "test", "tester", "")
        assert b'fields are filled.' in rv.data
        rv = self.register("", "", "", "", "")
        assert b'fields are filled.' in rv.data

    #Testing if its possible to register a user
    def test_register_user_with_valid_data(self):
        self.register("asd@asd.com", "test", "test", "test", "test")
        user = database.get_session().query(User).filter(User.email == "asd@asd.com").first()
        assert user is not None

    def test_remove_user_from_database(self):
        user = database.get_session().query(User).filter(User.email == "asd@asd.com").first()
        if user is None:
            return
        database.get_session().execute("DELETE FROM users WHERE email = 'asd@asd.com'")
        database.get_session().commit()
        user = database.get_session().query(User).filter(User.email == "asd@asd.com").first()
        assert user is None

if __name__ == '__main__':
    unittest.main()