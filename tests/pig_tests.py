import os, pig, unittest
from pig.views import get_divisions, pig_key
from pig.db.models import *
from pig.db.database import *
from flask import Flask

class PigTestCase(unittest.TestCase):


    def setUp(self):
        pig.app.config['TESTING'] = True
        self.app = pig.app.test_client()
        self.database = database(Flask(__name__))

    def login(self,username,password):
        return self.app.post("/login", data=dict(Username=username,Password=password),follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    # A helper method to setup the connection to the postgresDB on heroku
    def setup_db(self, uri="postgres://wtsceqpjdsbhxw:34df69f4132d39ea5b95e52822d6dedc8e3eb368915cb8888526f896f21bce75@ec2-54-75-229-201.eu-west-1.compute.amazonaws.com:5432/dfa7tvu04d7t6i" ):
        temp = database(Flask(__name__))
        temp.set_uri(uri)
        return temp

    # Testing connection to db with invalid uri, this is done by setting up a new connection to the db, and then changing the uri,
    # see setup_db.
    def test_connect_to_db_with_invalid_uri(self):
        data = None
        database = self.setup_db(uri = "postgres://wtsceqpjdsbhxw")
        try:
            data = database.get_session().query(User).first()
        except Exception as e1:
            print(e1)
        finally:
            assert data is None

    def test_connect_to_db_with_valid_uri(self):
        data = None
        database = self.setup_db()
        try:
            data = database.get_session().query(User).first()
        except Exception as e:
            print(e)
        finally:
            assert data is not None


    def test_login_invalid_username(self):
        self.register('valid@email.com','password','password','firstname','firstname')
        rv = self.login('invalid','password')

        assert b'firstname' not in rv.data

    def test_login_invalid_password(self):
        self.register('valid@email.com','password','password','firstname','lastname')
        rv = self.login('valid@email.com','wrong password')

        assert b'firstname' not in rv.data


    def test_login_and_logout_valid_username_and_password(self):
        self.register('valid@email.com','password','password','firstname','lastname')
        rv = self.login('valid@email.com','password')

        assert b'firstname' in rv.data

        rv = self.logout()
        assert b'firstname' not in rv.data

    def test_create_division(self):
        pass

    #A helper method that sends a post request to the register page containing all of the registration-info
    def register(self, email, password, password_confirm, first_name, last_name):
        return self.app.post("/register", data=dict(Email=email, Password=password, PasswordConfirm=password_confirm, FirstName=first_name, LastName=last_name))

    def delete_user(self, email):
        self.database.get_session().execute("DELETE FROM users WHERE email = '" + email + "'")
        self.database.get_session().commit()

    def create_division(self, name, creator_id):
        division = Division(name=name, creator_id=creator_id)
        self.database.get_session().add(division)
        self.database.get_session().commit()

    def delete_division(self, id):
        self.database.get_session().execute("DELETE FROM user_division WHERE division_id = " + str(id))
        self.database.get_session().execute("DELETE FROM division WHERE id = " + str(id))
        self.database.get_session().commit()

    def get_user(self, email):
        return self.database.get_session().query(User).filter(User.email == email).first()

    def go_to_division(self, link):
        return self.app.get("/" + link)


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
        user = self.database.get_session().query(User).filter(User.email == "asd@asd.com").first()
        assert user is not None

    def test_remove_user_from_database(self):
        user = self.get_user("asd@asd.com")
        if user is None:
            return
        self.delete_user("asd@asd.com")
        user = self.get_user("asd@asd.com")
        assert user is None

    def test_register_user_as_student_for_division(self):
        self.register("tester@asd.com", "test", "test", "Asd", "asdtest")
        self.register("tester1@asd.com", "test", "test", "Asd1", "asdtest")
        user = self.get_user("tester@asd.com")
        user1 = self.get_user("tester1@asd.com")
        self.create_division("testing_division", user.id)
        division = self.database.get_session().query(Division).filter(Division.creator_id == user.id, Division.name == "testing_division").first()
        self.login("tester1@asd.com", "test")
        link = get_divisions.get_link(pig_key, division.name, division.id, 1)
        rv = self.go_to_division(link)
        assert b'registered you as a' in rv.data
        self.delete_division(division.id)
        self.delete_user(user.email)
        self.delete_user(user1.email)





if __name__ == '__main__':
    unittest.main()