import matplotlib.pyplot as plt
import numpy as np
import random
import statistics as st
import math


def get_points_at_sorting_process_pct(points_moves, pct):
    return [move[int(pct * len(move))] for move in points_moves]

def get_two_points_distance(p1, p2):
    dimention = len(p1)
    distance = 0
    for i in range(dimention):
        distance += (p1[i] - p2[i]) ** 2
    return math.sqrt(distance)

def get_max_distance_in_cloud(points):
    max_dis = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            max_dis = max(max_dis, get_two_points_distance(points[i], points[j]))
    return max_dis

def get_monotonicity(arr):
    prev = 100000000
    res = 0
    for n in arr:
        if n > prev:
            res += 1 
        prev = n 
    return res

def get_avg_monotonicy(points):
    sum = 0
    for p in points:
        sum += get_monotonicity(p)
    return sum / len(points)

def get_monotonicity_change(file):
    points_moves = np.load(file, allow_pickle=True,)
    points_num = points_moves
    monotonicities = []
    for p in range(100):
        pct = p * 0.01
        points = get_points_at_sorting_process_pct(points_moves, pct)
        monotonicities.append(get_avg_monotonicy(points))
    return monotonicities

def point_cloud_size_change(file):
    points_moves = np.load(file, allow_pickle=True,)
    points_num = points_moves
    cloud_diameters = []
    for p in range(100):
        pct = p * 0.01
        point_cloud = get_points_at_sorting_process_pct(points_moves, pct)
        cloud_diameters.append(get_max_distance_in_cloud(point_cloud))
    
    return cloud_diameters



cloud_diameters = point_cloud_size_change('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_20_points_sorting_steps.npy')
bubble_monotonicity_change = get_monotonicity_change('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_20_points_sorting_steps.npy')

print(np.corrcoef(cloud_diameters, bubble_monotonicity_change)[0, 1])

selection_cells_cloud_diameters = point_cloud_size_change('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_20_points_sorting_steps.npy')
selection_monotonicity_change = get_monotonicity_change('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_20_points_sorting_steps.npy')

print(np.corrcoef(selection_cells_cloud_diameters, selection_monotonicity_change)[0, 1])


plt.figure()
plt.title("20D Points CLoud Size Change")
plt.xlabel('sorting percentage')
plt.ylabel('cloud diameter')
x = [n for n in range(100)]
plt.plot(x, cloud_diameters, color='r', label="bubble cell cloud size change",)
plt.plot(x, selection_cells_cloud_diameters, color='b', label="selection cell cloud size change",)
plt.legend(loc='best')
plt.show()







