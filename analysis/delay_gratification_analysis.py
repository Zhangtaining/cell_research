import matplotlib.pyplot as plt
import numpy as np
import random
import statistics as st
import pandas as pd
import math
import copy
from tabulate import tabulate
from statsmodels.stats.weightstats import ztest

# def get_monotonicity(arr):
#     prev = 100000000
#     res = 0
#     for n in arr:
#         if n > prev:
#             res += 1 
#         prev = n 
#     return res

def get_monotonicity(arr):
    monotonicity_value = 0
    prev = arr[0]
    for i in range(1, len(arr)):
        if arr[i] < prev:
            monotonicity_value += 1
        prev = arr[i]
    return monotonicity_value

def get_sorting_score(arr):
    expected_arr = copy.deepcopy(arr)
    expected_arr.sort()
    # print(sum([abs(a-b) for (a, b) in zip(expected_arr, arr)]))
    return sum([1 if a != b else 0 for (a, b) in zip(expected_arr, arr)])

def dedup(arr):
    res = []
    for x in arr:
        if len(res) == 0 or res[-1] != x:
            res.append(x)
    return res  

def get_discrepency_arr(arr):
    arr = dedup(arr)
    # print(arr)
    temp = []
    for i in range(1, len(arr)):
        temp.append(arr[i] - arr[i - 1])
    
    res = []
    if len(temp) == 0:
        return [0]
    x = temp[0]
    for i in range(1, len(temp)):
        if temp[i-1] * temp[i] > 0:
            x += temp[i]
        if temp[i-1] * temp[i]  <= 0:
            res.append(x)
            x = temp[i]
    res.append(x)
    return res

def get_first_pos(arr):
    for i in range(len(arr)):
        if arr[i] > 0:
            return i 
    return len(arr)

def max_wandering_range(arr):
    d_arr = get_discrepency_arr(arr)
    first_pos_index = get_first_pos(d_arr)
    res = -1000 
    i = first_pos_index
    if i >= len(d_arr) - 1:
        return 0
    while i < len(d_arr):
        j = i + 1
        if not (j <  len(d_arr)) or d_arr[j] > 0:
            return res 
        res = max(res, -(d_arr[j] + d_arr[i]))
        # res = max(res, d_arr[i])
        i += 2 
    return res

def avg_wandering_range(arr):
    d_arr = get_discrepency_arr(arr)
    # print(d_arr)
    first_pos_index = get_first_pos(d_arr)
    res = 0 
    n = 0
    i = first_pos_index
    changes = []
    if i >= len(d_arr) - 1:
        return 0
    # print(d_arr)
    while i < len(d_arr):
        j = i + 1
        if not (j <  len(d_arr)) or d_arr[j] > 0:
            return res 
        # res = max(res, -(d_arr[j] + d_arr[i]))
        # res = max(res, d_arr[i])
        if d_arr[i] < 0:
            print(d_arr[i])

        # res += d_arr[i]
        change = (-(d_arr[j] + d_arr[i])) / d_arr[i]
        changes.append(change)
        # if change > 1:
        res += change
        n += 1
        i += 2 
    if n == 0:
        return 0
    # print(changes)
    # print(res/n)
    return res / n

def get_max_delay_gratification(steps):
    monotonicity_changes = [get_monotonicity(step) for step in steps if len(step) > 0]
    # print(monotonicity_changes)
    # monotonicity_changes = [get_sorting_score(step) for step in steps if len(step) > 0]
    if len(monotonicity_changes) == 0:
        return 0
    # return max_wandering_range(monotonicity_changes)
    return avg_wandering_range(monotonicity_changes)

def get_delay_gratification_arr(file):
    experiments = np.load(file, allow_pickle=True,)
    results = []
    for exp_steps in experiments:
        if len(exp_steps) == 0:
            continue
        # print(exp_steps)
        results.append(get_max_delay_gratification(exp_steps))
    return results

def get_delay_gratification_arr_from_original_algo(file):
    experiments = np.load(file, allow_pickle=True,)
    # return [max_wandering_range(exp_record) for exp_record in experiments]
    return [avg_wandering_range(exp_record) for exp_record in experiments]


bubble_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_steps_100exps.npy')
selection_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_sorting_steps_100exps.npy')
insertion_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/insertion_sort_sorting_steps_100exps.npy')

bubble_with_frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_with_frozen_steps_100exps.npy')
selection_with_frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_sorting_with_frozen_steps_100exps.npy')
insertion_with_frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/insertion_sort_sorting_with_frozen_steps_100exps.npy')

bubble_with_2frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_with_2frozen_steps_100exps.npy')
selection_with_2frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_sorting_with_2frozen_steps_100exps.npy')
insertion_with_2frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/insertion_sort_sorting_with_2frozen_steps_100exps.npy')

bubble_with_3frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_with_3frozen_steps_100exps.npy')
insertion_with_3frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/insertion_sort_sorting_with_3frozen_steps_100exps.npy')
selection_with_3frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_sorting_with_3frozen_steps_100exps.npy')

bubble_with_4frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_with_4frozen_steps_100exps.npy')
insertion_with_4frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/insertion_sort_sorting_with_4frozen_steps_100exps.npy')
selection_with_4frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_sorting_with_4frozen_steps_100exps.npy')

bubble_with_5frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_with_5frozen_steps_100exps.npy')
insertion_with_5frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/insertion_sort_sorting_with_5frozen_steps_100exps.npy')
selection_with_5frozen_delay_gratification_arr = get_delay_gratification_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_sorting_with_5frozen_steps_100exps.npy')


original_bubble_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_bubble_sort_with_0frozen_steps_100exps.npy')
original_selection_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_selection_sort_with_0frozen_steps_100exps.npy')
original_insertion_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_insertion_sort_with_0frozen_steps_100exps.npy')

original_bubble_with_frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_bubble_sort_with_1forzen_sorting_steps_100exps.npy')
original_selection_with_frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_selection_sort_with_1frozen_sorting_steps_100exps.npy')
original_insertion_with_frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_insertion_sort_with_1frozen_sorting_steps_100exps.npy')

original_bubble_with_2frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_bubble_sort_with_2forzen_sorting_steps_100exps.npy')
original_selection_with_2frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_selection_sort_with_2frozen_sorting_steps_100exps.npy')
original_insertion_with_2frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_insertion_sort_with_2frozen_sorting_steps_100exps.npy')

original_bubble_with_3frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_bubble_sort_with_3forzen_sorting_steps_100exps.npy')
original_selection_with_3frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_selection_sort_with_3frozen_sorting_steps_100exps.npy')
original_insertion_with_3frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_insertion_sort_with_3frozen_sorting_steps_100exps.npy')

original_bubble_with_4frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_bubble_sort_with_4forzen_sorting_steps_100exps.npy')
original_selection_with_4frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_selection_sort_with_4frozen_sorting_steps_100exps.npy')
original_insertion_with_4frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_insertion_sort_with_4frozen_sorting_steps_100exps.npy')

original_selection_with_5frozen_delay_gratification_arr = get_delay_gratification_arr_from_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_selection_sort_with_5frozen_sorting_steps_100exps.npy')

def fetch_data_to_display(algo, data):
    return algo, min(data), st.median(data), max(data), np.average(data), np.std(data)

data = pd.DataFrame(
    [
        fetch_data_to_display('Bubble', bubble_delay_gratification_arr),
        fetch_data_to_display('Bubble with frozen', bubble_with_frozen_delay_gratification_arr),
        fetch_data_to_display('Bubble with 2 frozen', bubble_with_2frozen_delay_gratification_arr),
        fetch_data_to_display('Bubble with 3 frozen', bubble_with_3frozen_delay_gratification_arr),
        fetch_data_to_display('Bubble with 4 frozen', bubble_with_4frozen_delay_gratification_arr),
        fetch_data_to_display('Bubble with 5 frozen', bubble_with_5frozen_delay_gratification_arr),
        fetch_data_to_display('Original Bubble', original_bubble_delay_gratification_arr),
        fetch_data_to_display('Original Bubble with frozen', original_bubble_with_frozen_delay_gratification_arr),
        fetch_data_to_display('Original Bubble with 2 frozen', original_bubble_with_2frozen_delay_gratification_arr),
        fetch_data_to_display('Original Bubble with 3 frozen', original_bubble_with_3frozen_delay_gratification_arr),
        fetch_data_to_display('Insertion', insertion_delay_gratification_arr),
        fetch_data_to_display('Insertion with frozen', insertion_with_frozen_delay_gratification_arr),
        fetch_data_to_display('Insertion with 2 frozen', insertion_with_2frozen_delay_gratification_arr),
        fetch_data_to_display('Insertion with 3 frozen', insertion_with_3frozen_delay_gratification_arr),
        fetch_data_to_display('Insertion with 4 frozen', insertion_with_4frozen_delay_gratification_arr),
        fetch_data_to_display('Insertion with 5 frozen', insertion_with_5frozen_delay_gratification_arr),
        fetch_data_to_display('Original Insertion', original_insertion_delay_gratification_arr),
        fetch_data_to_display('Original Insertion with frozen', original_insertion_with_frozen_delay_gratification_arr),
        fetch_data_to_display('Original Insertion with 2 frozen', original_insertion_with_2frozen_delay_gratification_arr),
        fetch_data_to_display('Original Insertion with 3 frozen', original_insertion_with_2frozen_delay_gratification_arr),
        fetch_data_to_display('Selection', selection_delay_gratification_arr),
        fetch_data_to_display('Selection with frozen', selection_with_frozen_delay_gratification_arr),
        fetch_data_to_display('Selection with 2 frozen', selection_with_2frozen_delay_gratification_arr),
        fetch_data_to_display('Selection with 3 frozen', selection_with_3frozen_delay_gratification_arr),
        fetch_data_to_display('Selection with 4 frozen', selection_with_4frozen_delay_gratification_arr),
        fetch_data_to_display('Selection with 5 frozen', selection_with_5frozen_delay_gratification_arr),
        fetch_data_to_display('Original Selection', original_selection_delay_gratification_arr),
        fetch_data_to_display('Original Selection with frozen', original_selection_with_frozen_delay_gratification_arr),
        fetch_data_to_display('Original Selection with 2 frozen', original_selection_with_2frozen_delay_gratification_arr),
        fetch_data_to_display('Original Selection with 3 frozen', original_selection_with_3frozen_delay_gratification_arr),
        fetch_data_to_display('Original Selection with 4 frozen', original_selection_with_4frozen_delay_gratification_arr),
        fetch_data_to_display('Original Selection with 5 frozen', original_selection_with_5frozen_delay_gratification_arr),
    ], columns = ['Sorting algorithm', 'Min', 'Median', 'Max', 'Avg', 'Std dev'])

print(data)
