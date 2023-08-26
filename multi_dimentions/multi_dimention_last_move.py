#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np
import math
import sys
import random
import copy


current_step = 1



def generate_n_dimention_array(n):
    return [random.randint(0, 100) for i in range(0, n)]


def make_move(arr):
    n = len(arr)
    i = random.randint(0, n - 1)
    new_arr = copy.deepcopy(arr)
    new_arr[i] = random.randint(0, 100)
    return new_arr

def get_color(current_step, n):
    cmap = plt.get_cmap('binary') 
    cnorm  = colors.Normalize(vmin=0, vmax=n)
    scalarMap = cmx.ScalarMappable(norm=cnorm, cmap=cmap)
    c = scalarMap.to_rgba(current_step)
    return c

# Don't need to generate the arr
# dimention = 10
# arr = generate_n_dimention_array(10)
# moves = [arr]
# for i in range(20):
#     a = make_move(arr)
#     moves.append(a)
#     arr = a
    
# prev_move = moves[0]
# points = []
# for i in range(1, len(moves)):
#     move = moves[i]
#     for d in range(0, len(move)):
#         if prev_move[d] != move[d]:
#             points.append([move[d], d])
#             break 
#     prev_move = move 
# z = np.array(points)
z = np.load('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_steps_for_1_exp.npy')
moves = z[0]

prev_move = moves[0]
points = []
for i in range(1, len(moves)):
    move = moves[i]
    print(move)
    for d in range(0, len(move)):
        if prev_move[d] != move[d]:
            points.append([move[d], d]) 
    prev_move = move 
z = np.array(points)

x = z[:,0] 
y = z[:,1]
s = range(1, len(x) + 1)
plt.figure()
for i in range(1, len(points)):
    current_points = points[i]
    prev_points = points[i-1]
    x = [prev_points[0],current_points[0] ]
    y = [prev_points[1],current_points[1] ]
    plt.plot(x, y, '-', color=get_color(i, len(points))) 

plt.xlabel('position')
plt.ylabel('dimention')
# ax = plt.axes(projection='3d')
# plt.plot(x, y, s)
# ax.set_xlabel('value')
# ax.set_ylabel('dimention')
# ax.set_zlabel('step')
plt.show()
