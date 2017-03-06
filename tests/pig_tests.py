import os, pig, unittest

class PigTestCase(unittest.TestCase):

    def setUp(self):
        pig.app.config['TESTING'] = True
        self.app = pig.app.test_client()


    def login(self,username,password):
        return self.app.post("/login", data=dict(Username=username,Password=password),follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

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

