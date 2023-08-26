from sklearn.manifold import TSNE
from keras.datasets import mnist
from sklearn.datasets import load_iris
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np
from numpy import reshape
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import random
import copy


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

arr = generate_n_dimention_array(10)
moves = [arr]
for i in range(20):
    a = make_move(arr)
    moves.append(a)
    arr = a


#x = np.array(moves)
loaded_data = np.load('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_steps_for_50_exps.txt.npy', allow_pickle=True,)
for idx in range(len(loaded_data)):

    data = loaded_data[idx]
    tsne = TSNE(n_components=2, perplexity=20, verbose=1, random_state=123)
    points = tsne.fit_transform(np.array(data))
    for i in range(1, len(points)):
        current_points = points[i]
        prev_points = points[i-1]
        x = [prev_points[0],current_points[0]]
        y = [prev_points[1],current_points[1]]
        plt.plot(x, y, '-', color=get_color(i, len(points))) 

        # df = pd.DataFrame()
        # df["x"] = z[:,0]
        # df["y"] = z[:,1]

        # sns.scatterplot(x="x", y="y",
        #                 data=df).set(title="n dimentions moving path")
        # sns.lineplot(data=df, x="x", y="y", estimator='max', color='red')

plt.show()