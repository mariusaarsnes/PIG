from pig.scripts.DividingAlgorithm import DividingAlgorithm, DataPoint
from random import random

n = 5
n_points = 25
cluster_size = 5

points = []
for id in range(n_points):
    point = [random() for i in range(n)]
    points.append(DataPoint(id, point))

clusters = DividingAlgorithm.k_means(points, cluster_size)

for cluster in clusters:
    print("Cluster:")
    for point in cluster.points:
        print("{}, ".format(point.id), end='')
    print()

print("\nNormalizing\n")
