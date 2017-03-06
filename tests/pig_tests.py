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

if __name__ == '__main__':
    unittest.main()