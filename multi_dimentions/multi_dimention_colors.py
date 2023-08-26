#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import math
import sys
import random


def calculate_color(num):
    rgb = int(255 * (num / 100))
    return [rgb, rgb, rgb]


def calculate_angle(dimention):
    return 360 / dimention  


def generate_n_dimention_array(n):
    return [random.randint(0, 100) for i in range(0, n)]


def make_move(arr):
    n = len(arr)
    i = random.randint(0, n - 1)
    arr[i] = random.randint(0, 100)
    return arr

def main(argv):
    dimention = 10
    plt.figure()
    plt.title("Bubble Sort Multi Dimentions Visualization")
    plt.xlabel('sorting steps')
    plt.ylabel('dimention')
    z = np.load('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_steps_for_1_exp.npy')
    moves = z[0]
    for i in range(int(len(moves)/10) + 1):
        y = 1
        arr = moves[min(i*10, len(moves) - 1)]
        for v in arr:
            plt.scatter(min(i*10, len(moves) - 1), y, s=250, c=v, marker='s', cmap='hsv', norm=colors.Normalize(vmin=0, vmax=100.0))
            y+=1
        if i*10 >= len(moves):
            break
    plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])