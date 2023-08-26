#import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import math
import sys
import random

def calculate_position(angle, length, t):
    x = math.cos(math.radians(angle)) * length 
    y = math.sin(math.radians(angle)) * length
    return (x, y, t)


def calculate_angle(dimention):
    return 360 / dimention  


def generate_n_dimention_array(n):
    return [random.randint(0, 100) for i in range(0, n)]


def make_move(arr):
    n = len(arr)
    arr[random.randint(0, n)] = random.randint(0, 100)
    return arr

def main(argv):
    dimention = 10
    arr = generate_n_dimention_array(dimention)
    angle = calculate_angle(dimention)
    points = [calculate_position(i*angle, arr[i], 0) for i in range(len(arr))]
    points.append(points[0])
    arr2 = make_move(arr)
    points2 = [calculate_position(i*angle, arr[i], 1) for i in range(len(arr2))]
    points.extend(points2)
    points.append(points2[0])

    xs, ys, zs = zip(*points)

    plt.figure()
    plt.axes(projection='3d')
    plt.plot(xs, ys, zs) 
    plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])