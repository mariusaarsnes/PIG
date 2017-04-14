from pig.scripts.PartitionAlg import PartitionAlg, DataPoint
from random import random

def print_clusters(clusters):
    for cluster in clusters:
        print("Cluster:")
        for point in cluster.points:
            print("{}, ".format(point.id), end='')
        print()


n = 5
n_points = 25
cluster_size = 5

print("\nPartitioning\n")
points = []
for id in range(n_points):
    point = [random() for i in range(n)]
    points.append(DataPoint(id, point))

clusters = PartitionAlg.k_means(points, cluster_size)

print_clusters(clusters)

print("\nNormalizing\n")

PartitionAlg.normalize(clusters, cluster_size)

print_clusters(clusters)


for cluster in clusters:
    assert len(cluster.points) == cluster_size
