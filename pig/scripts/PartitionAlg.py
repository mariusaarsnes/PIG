import sys
import random
import math

class PartitionAlg:
    def __init__(self, database, DbGetters):
        self.database = database
        self.db_getters = DbGetters
        self.Division = DbGetters.Division
        self.Value = DbGetters.Value
        self.Group = DbGetters.Group
        self.user_division_parameter_value = DbGetters.user_division_parameter_value
        self.user_group = DbGetters.user_group
        self.user_division = DbGetters.user_division

    def create_groups(self, current_user, division_id):
        members = self.db_getters.get_groupless_users(division_id)
        division = self.database.get_session().query(self.Division)\
                    .filter(self.Division.id == division_id).first();

        data = self.prepare(division)
        clusters = PartitionAlg.k_means(data, division.group_size)
        PartitionAlg.normalize(clusters, division.group_size)

        i = 0
        for cluster in clusters:
            print("Cluster({})".format(len(cluster.points)), file=sys.stderr)
            # Insert group into database
            group = self.Group(division_id = division.id, number = i)
            self.database.get_session().add(group)
            self.database.get_session().commit()
            i += 1

            # Insert members into group
            for point in cluster.points:
                self.database.get_session().execute(f"INSERT INTO user_group VALUES({point.id}, {group.id})")


    # Create a structure that can be used as input to k_means
    # -> list of DataPoints
    def prepare(self, division):
        # Structure for temporarily storing the values of the different users:
        # hash map from user id to vector of parameters
        users = {}

        for parameter in division.parameters:
            assert parameter.number_param is not None # Current assumption
            min = parameter.number_param.min
            max = parameter.number_param.max
            q = 1.0 / (max - min) # Just for arithmetic efficiency

            values = self.database.get_session().query(self.user_division_parameter_value)\
                    .filter(self.user_division_parameter_value._columns.get("division_id") == division.id)\
                    .filter(self.user_division_parameter_value._columns.get("parameter_id") == parameter.id)\
                    .all()
            for value in values:
                # Push the value back to the user's vector
                if not value.user_id in users:
                    users[value.user_id] = []

                val = self.database.get_session().query(self.Value)\
                        .filter(self.Value.id == value.value_id)\
                        .first().value
                # Normalize the value - float number [0, 1]
                val = (val - min)  * q
                users[value.user_id].append(val)

            # (TODO: Ensure that the same amount of values is registered for each user at this point)

        # Eliminate users that are already in a group
        for user_id in list(users):
            participations = self.database.get_session().query(self.user_group)\
                    .filter(self.user_division._columns.get("user_id") == user_id)
            for participation in participations:
                group = self.database.get_session().query(self.Group)\
                        .filter(self.Group.id == participation.group_id)\
                        .first()
                if group.division_id == division.id:
                    users.pop(user_id, None)

        return [DataPoint(id, point) for (id, point) in users.items()]



    # Returns list of lists of DataPoints
    def k_means(points, cluster_size):
        if len(points) == 0:
            return []
        n = len(points[0].point) # number of elements in a point

        n_clusters = math.ceil(len(points) / cluster_size)

        # Initialize the clusters with random `mean`s, and no points
        clusters = [Cluster([random.random() for i in range(n)], [])\
                        for i in range(n_clusters)]
        prev_clusters = clusters

        assert len(clusters) != 0

        while True: # Will converge
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

    # Make groups be of a target size
    def normalize(clusters, target_size):
        neighbors = [[] for i in range(len(clusters))]
        for i, cluster in enumerate(clusters):
            # Needed to know the order, for later
            cluster.index = i
            # Make a list of the other clusters sorted by distance (sum squared)
            # Beware that the first element will be the current cluster.
            neighbors[i] = sorted(clusters, key = lambda other: sum_squares(cluster.mean, other.mean))

        MAX_ITERATIONS = 50 # I don't know if it always converges
        iterations = 0
        # Algorithm to normalize clusters:
        # Repeat, for as long as there is no change:
        #   For each cluster:
        #       find the nearest neighbor that has a different number of points (should differ at least by 2)
        #       exchange a point with this one - whichever direction is needed

        # There is another constraint on the exchange: it can only happen if it doesn't compromise the size
        #       of the cluster with the smallest order of the two
        # "Compromise the size" meaning to take the size further away from the target size.

        while True:
            change = False
            for i, cluster in enumerate(clusters):
                for neighbor in neighbors[i][1:]:
                    # Prioritising the cluster with the lowest index.
                    leftmost = cluster if cluster.index < neighbor.index else neighbor
                    rightmost = cluster if cluster.index > neighbor.index else neighbor

                    # Rightmost can only get its will if it doesn't ruin it for leftmost
                    if len(leftmost.points) == target_size:
                        continue
                    elif len(leftmost.points) < target_size and len(rightmost.points) > 0:
                        leftmost.steal(rightmost)
                        change = True
                        continue

                    if len(leftmost.points) - len(rightmost.points) > 1:
                        rightmost.steal(leftmost)
                        change = True
                        break
                    elif len(leftmost.points) - len(rightmost.points) < -1:
                        leftmost.steal(rightmost)
                        change = True
                        break

            if not change or iterations > MAX_ITERATIONS:
                break
            iterations += 1

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

    # 'Steal' the point of `other` which is closest to `self.mean`
    def steal(self, other):
        # Find the index of the point closest to self.mean
        closest_point_i = min_index(other.points, lambda point: sum_squares(point.point, self.mean))
        self.points.append(other.points[closest_point_i])
        del other.points[closest_point_i]




def sum_squares(vec1, vec2):
    sum = 0
    for i in range(len(vec1)):
        sum += (vec1[i] - vec2[i])**2
    return sum

# Applies transform to each element in the array, and picks the index of the minimum result
def min_index(array, transform):
    assert len(array) != 0
    min_index = -1
    min_value = float("inf")
    for i, element in enumerate(array):
        new_value = transform(element)
        if new_value < min_value:
            min_value = new_value
            min_index = i
    return min_index

