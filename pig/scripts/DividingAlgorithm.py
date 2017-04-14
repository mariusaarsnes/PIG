import sys
import random

class DividingAlgorithm:
    def __init__(self, database, DbGetters):
        self.database = database
        self.db_getters = DbGetters
        self.Division = DbGetters.Division
        self.Value = DbGetters.Value
        self.user_division_parameter_value = DbGetters.user_division_parameter_value

    def create_groups(self, current_user, division_id):
        members = self.db_getters.get_groupless_users(division_id)
        division = self.database.get_session().query(self.Division)\
                    .filter(self.Division.id == division_id).first();

        data = self.prepare(division)
        clusters = DividingAlgorithm.k_means(data, division.group_size)
        for cluster in clusters:
            print("Cluster: {}".format(cluster))


    # Create a structure that can be used as input to k_means
    # -- list of DataPoints
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
                users[value.user_id].append(val.value / 10.0) # TODO normalize properly (not assuming 0-10)
            # TODO: Ensure that all users are at the same 'level' here

        return [DataPoint(id, point) for (id, point) in users.items()]



    # Returns list of lists of DataPoints
    def k_means(points, cluster_size):
        n = len(points[0].point) # number of elements in a point

        n_clusters = int(len(points) / cluster_size)

        # Initialize the clusters with random `mean`s, and no points
        clusters = [Cluster([random.random() for i in range(n)], [])\
                        for i in range(n_clusters)]
        prev_clusters = clusters

        while True:
            print("Iteration")
            # Reset clusters
            for cluster in clusters:
                cluster.points = []

            # Reupdate clusters based on their means
            for point in points:
                cluster_i = min_index(clusters, lambda cluster: sum_squares(cluster.mean, point.point))
                clusters[cluster_i].points.append(point)

            # Reupdate means
            for cluster in clusters:
                cluster.mean = cluster.update_mean()


            # Check whether to terminate
            if clusters == prev_clusters:
                break
            prev_clusters = clusters

        # Convert from points index, to user id
        return clusters

"""
    # Make groups be of a target size
    def normalize(clusters, target_size):
        while True:
            for cluster in clusters
"""

class DataPoint:
    def __init__(self, id, point):
        self.id = id
        self.point = point

class Cluster:
    def __init__(self, mean, points):
        self.mean = mean
        self.points = points # list(DataPoint)

    def update_mean(self):
        if len(self.points) == 0:
            return self.mean

        n = len(self.points[0].point)
        sum = [0] * n
        for point in self.points:
            for j, component in enumerate(point.point):
                sum[j] += component
        for i, component in enumerate(sum):
            sum[i] = component / len(self.points)
        return sum


def sum_squares(vec1, vec2):
    sum = 0
    for i in range(len(vec1)):
        sum += (vec1[i] - vec2[i])**2
    return sum

# Applies transform to each element in the array, and picks the index of the minimum result
def min_index(array, transform):
    min_index = -1
    min_value = float("inf")
    for i, element in enumerate(array):
        new_value = transform(element)
        if new_value < min_value:
            min_value = new_value
            min_index = i
    assert min_index != -1
    return min_index

