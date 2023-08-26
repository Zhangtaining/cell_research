import matplotlib.pyplot as plt
import numpy as np
import random

def get_current_monotonicity(arr):
        monotonicity_value = 0
        prev = arr[0]
        for i in range(1, len(arr)):
            if arr[i] < prev:
                monotonicity_value += 1
            prev = arr[i]
        return monotonicity_value

def matrix_multiply(arr):
    list2 = np.array([n for n in range(1, 101)]).reshape(100, 1)
    return np.dot(arr, list2)

def random_pick_color():
    r = random.random()
    b = random.random()
    g = random.random()
    return (r, g, b)


plt.figure()
plt.xlabel('time')
plt.ylabel('monocity')
def plot_raw_data(file):
    loaded_data = np.load(file, allow_pickle=True,)
    for moves in loaded_data:
        monotonicities = [matrix_multiply(arr) for  arr in moves]
        x = [n for n in range(1, len(monotonicities) +1)]
        plt.plot(x, monotonicities, c=random_pick_color())
    plt.show()

plot_raw_data('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_p0_steps_for_50_exp.npy')
plot_raw_data('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_p25_steps_for_50_exp.npy')
plot_raw_data('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_p50_steps_for_50_exp.npy')
plot_raw_data('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_p75_steps_for_50_exp.npy')


