from pig.scripts.PartitionAlg import PartitionAlg, DataPoint, sum_squares

from random import random
import time

def print_clusters(clusters):
    for cluster in clusters:
        print("Cluster:")
        for point in cluster.points:
            print("{}, ".format(point.id), end='')
        print()

def get_stats(clusters):
    min = float("inf")
    max = 0
    for cluster in clusters:
        if len(cluster.points) < min:
            min = len(cluster.points)
        if len(cluster.points) > max:
            max = len(cluster.points)
    return min, max



n = 10
n_points = 100
cluster_size = 6

def test_performance():
    global n
    global n_points
    global cluster_size

    for i in range(100):
        points = []
        for id in range(n_points):
            point = [random() for i in range(n)]
            points.append(DataPoint(id, point))

        t = time.time()
        clusters = PartitionAlg.k_means(points, cluster_size)
        PartitionAlg.normalize(clusters, cluster_size)
        t = time.time() - t

        stats = get_stats(clusters)

        print("{} students: {}    group size min, max: ({}, {})".format(n_points, t, stats[0], stats[1]))

        n_points += 100

def test_accuracy():
    global n
    global n_points
    global cluster_size

    print("\nPartitioning\n")
    # Create data
    points = []
    for id in range(n_points):
        point = [random() for i in range(n)]
        points.append(DataPoint(id, point))

    # Partition
    clusters = PartitionAlg.k_means(points, cluster_size)
    print_clusters(clusters)
    print("\nNormalizing\n")

    # Normalize
    PartitionAlg.normalize(clusters, cluster_size)
    print_clusters(clusters)

    # Test normalizing
    for cluster in clusters[:-1]:
        assert len(cluster.points) == cluster_size

    # Test accuracy
    for i, cluster in enumerate(clusters):
        variation = 0
        for point in cluster.points:
            variation += sum_squares(cluster.mean, point.point)
        print(f"Cluster {i} variation: {variation}")


test_accuracy()
