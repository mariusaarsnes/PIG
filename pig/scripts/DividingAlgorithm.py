class DividingAlgorithm:

    def __init__(self, database, DbGetters):
        self.database = database
        self.db_getters = DbGetters
        self.Division = DbGetters.Division
        self.Value = DbGetters.Value
        self.user_division_parameter_value = DbGetters.user_division_parameter_value
        return

    def create_groups(self, current_user, division_id):
        members = self.db_getters.get_groupless_users(division_id)
        division = self.database.get_session().query(self.Division)\
                    .filter(self.Division.id == division_id).first();


        # TODO: Fetch all values to all the members

        # TODO: Generate groups based on who are good matches.
        data = self.prepare(division)
        self.k_means(data, division.group_size)
        return


    # Create a structure that can be used as input to k_means
    # list of <structs that have an id and a list of values>
    def prepare(self, division):

        # Structure for temporarily storing the values of the different users:
        # hash map from user id to vector of parameters
        users = {}

        for parameter in division.parameters:
            values = self.database.get_session().query(self.user_division_parameter_value)\
                    .filter(self.user_division_parameter_value._columns.get("division_id") == division.id)\
                    .filter(self.user_division_parameter_value._columns.get("parameter_id") == parameter.id)\
                    .all()
            for value in values:
                # Push the value back to the user's vector
                # TODO check if it's from a `member`/groupless
                if not value.user_id in users:
                    users[value.user_id] = []

                val = self.database.get_session().query(self.Value)\
                        .filter(self.Value.id == value.value_id)\
                        .first()
                users[value.user_id].append(val.value)
            # TODO: Ensure that all users are at the same 'level' here

        return users.items() # creates a list of (key, value) tuples


    def k_means(self, data, group_size):
        for user in data:
            print("values: %r" % user)
