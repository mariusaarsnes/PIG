class DividingAlgorithm:

    def __init__(self, database, DbGetters):
        self.database = database
        self.db_getters = DbGetters
        return

    def createGroups(self, current_user, division_id):
        members = self.db_getters.get_groupless_users(division_id)

        # TODO: Fetch all values to all the members

        # TODO: Generate groups based on who are good matches.

        return



