import pig, unittest
from pig.db.models import *
from pig.db.database import *
from pig.scripts.DivideGroupsToLeaders import DivideGroupsToLeaders
from pig.scripts.PartitionAlg import PartitionAlg, DataPoint, Cluster
from pig.scripts.DbGetters import *
from flask import Flask
from random import randint, random
from pig.scripts.Tasks import Tasks
from pig.scripts.RegisterUser import RegisterUser
from pig.login.RegistrationHandler import RegistrationHandler
from pig.scripts.CreateDivision import CreateDivision
from pig.login.LoginHandler import LoginHandler
from pig.scripts.Encryption import *
from passlib.hash import bcrypt

from sqlalchemy.sql.expression import func

from sqlalchemy import MetaData
meta = MetaData()

class PigTestCase(unittest.TestCase):

    def setUp(self):
        pig.app.config['TESTING'] = True

        self.app = pig.app.test_client()
        self.database = Database(Flask(__name__), "postgres://vvowlncwqspvuy:d33be97885"
                                                  "edd47261373cdc4366e0ecc0c7608658564e1"
                                                  "59f19d84801b05145@ec2-79-125-2-69.eu-west-1"
                                                  ".compute.amazonaws.com:5432/d76s6hbvr5lsfb")
        self.db_getters = DbGetters(
            self.database, User, Division, Group, Parameter, Value, NumberParam, EnumVariant,
            user_division, user_group, division_parameter, parameter_value, user_division_parameter_value)

        self.tasks = Tasks(
            self.database, User, Division, Group, Parameter, Value, NumberParam, EnumVariant,
            user_division, user_group, division_parameter, parameter_value, user_division_parameter_value)

        self.divide_groups_to_leaders = DivideGroupsToLeaders(self.database, Division, user_division, self.db_getters)
        self.registration_handler = RegistrationHandler(self.database, User)
        self.division_creator = CreateDivision(self.database, Division, Parameter, NumberParam, EnumVariant)
        self.division_registrator = RegisterUser(self.database,User,Division,user_division, Value, Parameter)
        self.login_handler = LoginHandler(self.database, User)
        self.alg = PartitionAlg(self.database, self.db_getters)

    #Clears the database between every test
    def tearDown(self):
        tables = ["user_division_parameter_value", "value","number_param", "enum_variant", "division_parameter", "parameter", "user_division", "user_group", "groups", "division", "users" ]
        for table in tables:
            self.database.get_session().execute("DELETE FROM " + table)
        self.database.get_session().commit()

    #Function that calls the site login function
    def login(self,username,password):
        return self.app.post("/login", data=dict(Username=username,Password=password),follow_redirects=True)

    #Function that calls the site logout function
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def show_divisions(self):
        return self.app.get('/show_divisions', follow_redirects=True)

    # A helper method to setup the connection to the postgresDB on heroku
    def setup_db(self, uri="postgres://vvowlncwqspvuy:d33be97885edd47261373cdc4366e0ecc"
                           "0c7608658564e159f19d84801b05145@ec2-79-125-2-69.eu-west-1."
                           "compute.amazonaws.com:5432/d76s6hbvr5lsfb"):
        temp = Database(Flask(__name__),uri)
        return temp

    #A helper method that sends a post request to the register page containing all of the registration-info
    def register(self, email, password, password_confirm, first_name, last_name):
        result = self.registration_handler.validate_form(
            form=dict(
                Email=email, Password=password,
                PasswordConfirm=password_confirm,
                FirstName=first_name,
                LastName=last_name))
        if result[0]:
            self.registration_handler.create_user(first_name, last_name, email, password)

    #Inserts user data into the database, and returns the user object
    def create_user(self, email, password, first_name, last_name):
        self.database.get_session().execute("INSERT INTO users (firstname,lastname,email,password) VALUES('" +first_name+"','" + last_name+"','" + email +"','"+bcrypt.hash(password)+"')")
        self.database.get_session().commit()
        return self.database.get_session().query(User).filter(User.email == email).first()

    #Creates a range of users (for tests that require a large amount of users)
    def create_users_with_given_parameters_for_usertype_and_count(self,type,count):
        for i in range(count):
            self.database.get_session().execute("INSERT INTO users (firstname,lastname,email,password) VALUES('first"+type+str(i)+"','last"+type+str(i)+"','"+type+str(i)+"@email.com','password')")
        self.database.get_session().commit()

    #Removes a user based on their email (PK)
    def delete_user(self, email):
        self.database.get_session().execute("DELETE FROM users WHERE email = '" + email + "'")
        self.database.get_session().commit()

    #Creates a new division and returns it object
    def create_division(self, name, creator_id):
        division = Division(name=name, creator_id=creator_id)
        self.database.get_session().add(division)
        self.database.get_session().commit()
        return self.database.get_session().query(Division).filter(Division.id == database.get_session().query(func.max(Division.id)).first()[0]).first()

    #Creates a new group with given leader, then returns its object
    def create_group(self, division, leader_id):
        group = Group(leader_id=leader_id)
        division.groups.append(group)
        self.database.get_session().commit()
        return self.database.get_session().query(Group).filter(Group.id == database.get_session().query(func.max(Group.id)).first()[0]).first()

    #Returns the first division it finds that belongs to the creator specified
    def get_division(self,name,creator_id):
        return self.database.get_session()\
            .query(Division).filter(Division.creator_id == creator_id, Division.name == name).first()

    #Deletes the division with the given id
    def delete_division(self, id):
        #self.database.get_session().execute("DELETE FROM user_division WHERE division_id = " + str(id))
        self.database.get_session().execute("DELETE FROM division WHERE id = " + str(id))
        self.database.get_session().commit()

    #Returns the user object with the given email
    def get_user(self, email):
        return self.database.get_session().query(User).filter(User.email == email).first()

    #Returns the users within an id range (To find the newly created users for certain tests)
    def get_users_where_id_is_larger_or_equal_to_parameter_and_in_interval(self,minVal,size):
        return self.database.get_session().query(User).filter(User.id>=minVal,User.id < minVal+size)

    #Deleted the users within the id range given
    def delete_users_where_id_is_larger_or_equal_to_parameter_and_in_interval(self,minVal,size):
        self.database.get_session().execute("DELETE FROM users WHERE id >= " + str(minVal) + " AND id <" + str(minVal+size))
        self.database.get_session().commit()

    #Goes to the site page given by the link
    def go_to_division(self, link):
        return self.app.get("/" + link)

    #Creates a new group for the given division
    def create_single_group_with_given_division_id(self, division_id):
        group = Group(division_id= division_id)
        self.database.get_session().add(group)
        self.database.get_session().commit()

    #Creates multiple groups for the given division
    def create_multiple_groups_with_given_division_id(self,division_id, count):
        for i in range(count):
            self.database.get_session().execute("INSERT INTO groups (division_id) VALUES('"+str(division_id)+"')")
        self.database.get_session().commit()

    #Gets all groups linked to the specified division
    def get_groups_using_only_division_id(self,division_id):
        return self.database.get_session().query(Group).filter(Group.division_id == division_id)

    #Links a list of users to a given division with the role Teaching Assistant (TA)
    def sign_up_users_for_division_as_leader(self,leaders,division_id):
        for leader in leaders:
            self.database.get_session().execute\
                ("INSERT INTO user_division (user_id, division_id,role) VALUES('"+str(leader.id)+ "','" + str(division_id)+"','TA')")
        self.database.get_session().commit()

    #Deletes all groups linked to the specified division
    def delete_all_groups_in_given_division(self,division_id):
        self.database.get_session().execute("DELETE FROM groups WHERE division_id ="+str(division_id))

    #Deletes all users linked to the given division id
    def delete_from_user_division_with_given_division_id(self,division_id,count):
        for i in range(count):
            self.database.get_session().execute("DELETE FROM user_division WHERE division_id=" + str(division_id))
        self.database.get_session().commit()

    #Returns the users linked to the given divisions
    def get_user_division_on_given_division_id(self,division_id):
        return self.database.get_session().query(user_division).filter(user_division._columns.get("division_id")==division_id).all()

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

    #Tests if it is able to connect to the database with right login information
    def test_connect_to_db_with_valid_uri(self):
        data = None
        database = self.setup_db()
        try:
            self.create_user("test@email.com","password","name","name")
            data = database.get_session().query(User).first()
        except Exception as e:
            print(e)
        finally:
            assert data is not None

    # Testing login with an invalid username
    def test_login_invalid_username(self):
        self.create_user('valid@email.com','password','firstname','firstname')
        rv = self.login('invalid','password')

        self.delete_user('valid@email.com')
        assert b'firstname' not in rv.data

    # Testing login with a valid username, but invalid password
    def test_login_invalid_password(self):
        self.create_user('valid@email.com','password','firstname','lastname')
        rv = self.login('valid@email.com','wrong password')

        self.delete_user('valid@email.com')
        assert b'firstname' not in rv.data

    # Testing login with valid username and password, and then logging out.
    def test_login_and_logout_valid_username_and_password(self):
        user = self.create_user('valid@email.com','password','firstname','lastname')
        response = self.login('valid@email.com','password')
        self.login_handler.get_user_with_id(user.id)
        assert '200' in response.status

        response = self.logout()
        assert '200' in response.status

    #Tests if the given states of the users are right.
    def test_valid_user_states(self):
        user = self.create_user('valid@email.com','password','firstname','lastname')
        self.login('valid@email.com','password')
        login_user = self.login_handler.get_user_with_id(user.id)
        assert login_user.is_active()
        assert not login_user.is_anonymous()
        assert login_user.is_authenticated()
        assert login_user.get_id() == user.id
        self.logout()

    #The methods below are pretty self explainatory; they all query the database and they are used by the testing methods
    #instead of them directly querying the database.
    def delete_user(self, email):
        self.database.get_session().execute("DELETE FROM users WHERE email = '" + email + "'")
        self.database.get_session().commit()

    #Creates a new division with given name and leader, then returns it
    def create_division(self, name, creator_id):
        division = Division(name=name, creator_id=creator_id)
        self.database.get_session().add(division)
        self.database.get_session().commit()
        return division

    #Deletes the division with the given id
    def delete_division(self, id):
        self.database.get_session().execute("DELETE FROM user_division WHERE division_id = " + str(id))
        self.database.get_session().execute("DELETE FROM division WHERE id = " + str(id))
        self.database.get_session().commit()

    #Returns the user with the given mail
    def get_user(self, email):
        return self.database.get_session().query(User).filter(User.email == email).first()


    def go_to_division(self, link):
        return self.app.get("/" + link)

    #Tests to make sure our simple queries actually retutrn what we expect
    def test_registering_division(self):
        user = self.create_user("email@email.com", "password", "First", "Last")
        current_user = self.login_handler.get_user_with_id(user.id)
        division = self.create_division("new_div", current_user.id)
        assert self.db_getters.get_all_divisions()[0] == division
        print(self.db_getters.get_all_divisions_where_creator(current_user))
        assert self.db_getters.get_all_divisions_where_creator(current_user)[0] == division
        assert self.db_getters.get_division(division.id) == division
        assert self.db_getters.get_all_divisions_where_leader(current_user) is None

    #Testing registration of a user with two different passwords
    def test_register_user_with_two_different_password_inputs(self):
        self.register("asd@asd.com", "test", "test1", "tester", "testing")
        user = self.get_user("asd@asd")
        assert user is None

    #Testing registration of a user with invalid email by checking if the feedback contains a part of the string it displays to the user
    #when entering the wrong email.
    def test_register_user_with_invalid_email(self):
        self.register("asd@asd", "test", "test", "tester", "testing")
        user = self.get_user("asd@asd")
        assert user is None

        self.register("asd@as@d", "test", "test", "tester", "testing")
        user = self.get_user("asd@asd")
        assert user is None

        self.register("as..d@asd", "test", "test", "tester", "testing")
        user = self.get_user("as..d@asd")
        assert user is None

    #Testing if it is possible to register a user with one ore more empty fields. It does this by following the redirect after posting the
    #registration form then checking if it received the exepcted output.
    def test_register_user_with_one_or_more_empty_fields(self):

        self.register("asd@asd.com", "", "test", "tester", "testing")
        user = self.get_user("asd@asd")
        assert user is None

        self.register("asd@asd.com", "test", "", "tester", "testing")
        user = self.get_user("asd@asd.com")
        assert user is None

        self.register("asd@asd.com", "test", "test", "", "testing")
        user = self.get_user("asd@asd.com")
        assert user is None

        self.register("asd@asd.com", "test", "test", "tester", "")
        user = self.get_user("asd@asd.com")
        assert user is None

    #Testing if its possible to register a user
    def test_register_user_with_valid_data(self):
        self.register("asd@asd.com", "test", "test", "test", "test")
        user = self.get_user("asd@asd.com")
        assert user is not None

    #Tests if it is able to remove a user from the database
    def test_remove_user_from_database(self):
        user = self.get_user("asd@asd.com")
        if user is None:
            return
        self.delete_user("asd@asd.com")
        user = self.get_user("asd@asd.com")
        assert user is None

    #Tests if its possible to create a division with the given parameters
    #Makes sure the parameters is inserted with the right values and attributes
    def test_create_division_with_parameters(self):
        user = self.create_user("Email@email.com", "Password", "First", "Last")
        self.division_creator.register_division(user.id, dict(
        Division="Division",
        Type1="Number",
        Min1="1",
        Max1="10",
        Size="5",
        Parameter1="Param name",
        Option1_1=""))
        division = self.database.get_session().query(Division).filter(Division.creator_id == user.id).first()
        assert division is not None
        assert division.name == "Division"
        parameter = self.database.get_session().query(Parameter).filter(Parameter.id == division_parameter._columns.get("parameter_id"),
                                                                        Division.id == division_parameter._columns.get("division_id")).first()
        assert parameter.description == "Param name"
        number_param = self.database.get_session().query(NumberParam).filter(NumberParam.parameter_id == parameter.id).first()
        assert number_param.min == 1
        assert number_param.max == 10

    #Tests registering up for a division
    #Checks if the users are signed up for the right division with right roles and right parameter values
    def test_register_for_division(self):
        user = self.create_user("Email@email.com", "Password", "First", "Last")
        registration_user1 = self.create_user("Register1@user.com", "Password", "Firstname", "Lastname")
        registration_user2 = self.create_user("Register2@user.com", "Password", "Firstname", "Lastname")
        self.division_creator.register_division(user.id, dict(
        Division="Division",
        Type1="Number",
        Min1="1",
        Max1="10",
        Size="5",
        Parameter1="Param name",
        Option1_1=""))
        division = self.database.get_session().query(Division).filter(Division.creator_id == user.id).first()
        param_id = self.database.get_session().query(Parameter).first().id
        form_dict = {}
        form_dict.update({ "DivisionName": "Division" })
        form_dict.update({ "DivisionId": division.id })
        form_dict.update({ "Parameter" + str(param_id): 5 })
        self.division_registrator.register_user(self.login_handler.get_user_with_id(registration_user1.id), division.id, "Student")
        self.division_registrator.register_user(self.login_handler.get_user_with_id(registration_user2.id), division.id, "TA")
        self.division_registrator.register_parameters(self.login_handler.get_user_with_id(registration_user2.id), form_dict)
        assert self.database.get_session().query(user_division).filter(user_division._columns.get("role") == "Student").first().user_id == registration_user1.id
        assert self.database.get_session().query(user_division).filter(user_division._columns.get("role") == "TA").first().user_id == registration_user2.id
        assert self.database.get_session().query(Value).filter(user_division_parameter_value._columns.get("user_id") == registration_user2.id,
                                                               user_division_parameter_value._columns.get("division_id") == division.id,
                                                               user_division_parameter_value._columns.get("parameter_id") == param_id).first().value == 5
    #Tests if it is able to register a certain user to a certain division through the site. It generates the link for the signup based on data from the page
    #Then follows the url and checks if it gets the desired output.

    """
    def test_register_user_as_student_for_division(self):
        pass
        self.register("tester@asd.com", "test", "test", "Asd", "asdtest")
        self.register("tester1@asd.com", "test", "test", "Asd1", "asdtest")
        user = self.get_user("tester@asd.com")
        user1 = self.get_user("tester1@asd.com")
        self.create_division("testing_division", user.id)
        division = self.database.get_session().query(Division).filter(Division.creator_id == user.id, Division.name == "testing_division").first()
        self.login("tester1@asd.com", "test")
        link = self.tasks.get_link(pig_key, division.name, division.id, 1)
        rv = self.go_to_division(link)
        assert b'registered you as a' in rv.data
        self.delete_division(division.id)
        self.delete_user(user.email)
        self.delete_user(user1.email)
    """

    #Tests the encryption
    def test_encryption(self):
        link = "This is a test"
        encrypted_link = encode("Key", link)
        assert link == decode("Key", encrypted_link)

    #Tests if it is able to get all the users that has signed up for a given division as user
    def test_get_all_users_with_values(self):
        user = self.create_user("Email@email.com", "Password", "First", "Last")
        registration_user2 = self.create_user("Register2@user.com", "Password", "Firstname", "Lastname")
        self.division_creator.register_division(user.id, dict(
        Division="Division",
        Type1="Number",
        Min1="1",
        Max1="10",
        Size="5",
        Parameter1="Param name",
        Option1_1=""))
        division = self.database.get_session().query(Division).filter(Division.creator_id == user.id).first()
        param_id = self.database.get_session().query(Parameter).first().id
        form_dict = {}
        form_dict.update({ "DivisionName": "Division" })
        form_dict.update({ "DivisionId": division.id })
        form_dict.update({ "Parameter" + str(param_id): 5 })
        self.division_registrator.register_user(self.login_handler.get_user_with_id(registration_user2.id), division.id, "TA")
        self.division_registrator.register_parameters(self.login_handler.get_user_with_id(registration_user2.id), form_dict)
        user_dict = self.db_getters.get_all_users_with_values(division.id)
        for (key, value) in user_dict.items():
            assert key.id == registration_user2.id
            assert value[0].value == 5

    def test_get_groupless_users(self):
        user = self.create_user("Email@email.com", "Password", "First", "Last")
        registration_user2 = self.create_user("Register2@user.com", "Password", "Firstname", "Lastname")
        self.division_creator.register_division(user.id, dict(
        Division="Division",
        Type1="Number",
        Min1="1",
        Max1="10",
        Size="5",
        Parameter1="Param name",
        Option1_1=""))
        division = self.database.get_session().query(Division).filter(Division.creator_id == user.id).first()
        self.database.get_session().execute("INSERT INTO user_division VALUES(" + str(registration_user2.id) + ", " + str(division.id) + ", 'Student')")
        self.database.get_session().commit()
        groupless_users = self.db_getters.get_groupless_users(division.id)
        assert groupless_users[0].id == registration_user2.id

    # TODO Superfluous test? Because leaders are given in PartitionAlg, and this is also tested.
    def test_divide_groups_to_leaders_with_varying_range_of_leaders_and_groups(self):
        group_count = randint(15, 25)
        leader_count = randint(3, 7)

        self.create_user("creator@email.com","password",'firstCreator','lastCreator')
        self.create_users_with_given_parameters_for_usertype_and_count("leader",leader_count)

        creator = self.get_user('creator@email.com')
        first_leader = self.get_user('leader0@email.com')
        leaders = self.get_users_where_id_is_larger_or_equal_to_parameter_and_in_interval(first_leader.id,leader_count)

        self.create_division("test division",creator.id)
        division = self.get_division("test division", creator.id)

        self.create_multiple_groups_with_given_division_id(division_id=division.id,count=group_count)

        self.sign_up_users_for_division_as_leader(leaders=leaders,division_id=division.id)


        self.divide_groups_to_leaders.assign_leaders_to_groups(current_user=creator,division_id=division.id)

        groups = self.db_getters.get_all_groups_in_division(creator, division.id)

        for element in groups:
            assert (element.leader_id >= first_leader.id and element.leader_id < first_leader.id + leader_count)

        self.delete_all_groups_in_given_division(division.id)
        self.delete_division(division.id)
        self.delete_user('creator@email.com')
        self.delete_users_where_id_is_larger_or_equal_to_parameter_and_in_interval(first_leader.id,leader_count)

    def test_alg(self):
        print("Testing algorithm")
        S = 25 # number of students
        L = 2 # the L first students will sign up as leaders
        P = 3 # number of parameters
        group_size = 6

        creator = self.create_user("creator@email.com", "Password", "mr", "creator");

        # Create students
        students = [self.create_user(f"student{u}@email.com", "Password", f"first{u}", f"last{u}")\
                    for u in range(S)]

        # Create division
        self.create_division("division for test_alg", creator.id)
        division = self.get_division("division for test_alg", creator.id)
        division.group_size = group_size

        parameters = [ Parameter(description=f"param{p}") for p in range(P) ]

        # Sign up students and leaders
        for student in students[:L]:
            self.database.get_session().execute(f"INSERT INTO user_division VALUES({student.id}, {division.id}, 'TA')")
        for student in students[L:]:
            self.database.get_session().execute(f"INSERT INTO user_division VALUES({student.id}, {division.id}, 'Student')")

        for parameter in parameters:
            spec = NumberParam(min=0, max=10)

            division.parameters.append(parameter)
            spec.parameter = parameter

            self.database.get_session().add(parameter)
            self.database.get_session().add(spec)
            self.database.get_session().commit()

            # Sign up students for division, with random values
            for student in students[L:]:
                value = Value(value=randint(0,10), description="")
                self.database.get_session().add(value)
                self.database.get_session().commit()
                self.database.get_session().execute(f"INSERT INTO user_division_parameter_value VALUES({student.id}, {division.id}, {parameter.id}, {value.id})")

        self.database.get_session().commit()

        # Run alg
        self.alg.create_groups(creator, division.id)

        # Check that all students are assigned a group
        for student in students:
            participation = self.database.get_session().query(user_group)\
                    .filter(user_division._columns.get("user_id") == student.id)\
                    .first()
            assert participation is not None
            group = self.database.get_session().query(Group)\
                    .filter(Group.id == participation.group_id)\
                    .first()
            assert group is not None


        groups = self.database.get_session().query(Group)\
                .filter(Group.division_id == division.id)\
                .all()

        print("-> Now testing that all groups have a TA")
        for group in groups:
            assert group.leader_id is not None

        print("-> Now testing accuracy - only one group can have a different size")
        deviant_found = False
        for group in groups:
            members = self.database.get_session().query(user_group)\
                    .filter(user_group._columns.get("group_id") == group.id).all()
            if len(members) != division.group_size:
                assert not deviant_found
                deviant_found = True

        print("-> Now testing idempotence")
        groups = self.database.get_session().query(Group)\
                .filter(Group.division_id == division.id)\
                .all()
        num_groups = len(groups)

        # Run alg
        self.alg.create_groups(creator, division.id)

        groups = self.database.get_session().query(Group)\
                .filter(Group.division_id == division.id)\
                .all()
        num_groups_after = len(groups)
        assert num_groups == num_groups_after



    def print_clusters(self, clusters):
        for cluster in clusters:
            print("Cluster:")
            for point in cluster.points:
                print("{}, ".format(point.id), end='')
            print()

    def test_alg_normalize(self):
        n = 5 # number of components of points
        n_points = 36
        n_groups = 6
        cluster_size = n_points / n_groups

        # Create data points
        points = []
        for id in range(n_points):
            point = [random() for i in range(n)]
            points.append(DataPoint(id, point))

        # Partition
        clusters = PartitionAlg.k_means(points, cluster_size)

        # Normalize
        PartitionAlg.normalize(clusters, cluster_size)

        # Check that we successfully normalized - so that all groups have the same size
        for cluster in clusters:
            assert len(cluster.points) == cluster_size


if __name__ == '__main__':
    unittest.main()
