import matplotlib.pyplot as plt
import numpy as np
import random
import statistics as st
import pandas as pd
import math
import copy
from tabulate import tabulate
import scipy.stats as stats
from statsmodels.stats.weightstats import ztest

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
        change = -(d_arr[j] + d_arr[i]) / d_arr[i]
        #if change > 0:
        res += change
        n += 1
        i += 2 
    if n == 0:
        return 0
    return res / n

def get_max_delay_gratification(steps):
    monotonicity_changes = [get_monotonicity(step) for step in steps if len(step) > 0]
    #monotonicity_changes = [get_sorting_score(step) for step in steps if len(step) > 0]
    if len(monotonicity_changes) == 0:
        return 0
    #return max_wandering_range(monotonicity_changes)
    return avg_wandering_range(monotonicity_changes)

def get_delay_gratification_arr(file):
    experiments = np.load(file, allow_pickle=True,)
    results = []
    for exp_steps in experiments:
        if len(exp_steps) == 0:
            continue
        results.append(get_max_delay_gratification(exp_steps))
    return results

def get_delay_gratification_arr_from_original_algo(file):
    experiments = np.load(file, allow_pickle=True,)
    return  [get_max_delay_gratification(exp_steps) for exp_steps in experiments if len(exp_steps) > 0]
    # return [max_wandering_range(exp_record) for exp_record in experiments]
# /Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_with_0frozen_cannot_move_steps_100exps.npy
# /Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_with_0frozen_cannot_move_sorting_steps_100exps.npy

def load_cell_view_data(algorithm, frozen_cell_number):
    return get_delay_gratification_arr(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{algorithm}_sorting_with_{frozen_cell_number}frozen_cannot_move_steps_100exps.npy")

def fetch_cell_view_data_to_display(algo, frozen_cell_number):
    data = load_cell_view_data(algo, frozen_cell_number)
    return f"{algo}", min(data), st.median(data), max(data), np.average(data), np.std(data)

def load_data(algorithm, frozen_cell_number):
    # /Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_bubble_sort_with_0frozen_cannot_move_sorting_steps_100exps.npy
    # /Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_bubble_sort_with_0forzen_cannot_move_sorting_steps_100exps.npy
    #/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_insertion_sort_with_0frozen_cannot_move_sorting_steps_100exps.npy
    #/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_insertion_sort_with_0forzen_cannot_move_sorting_steps_100exps.npy
    return get_delay_gratification_arr_from_original_algo(f'/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{algorithm}_with_{frozen_cell_number}frozen_cannot_move_sorting_records_100exps.npy')

def fetch_data_to_display(algo, frozen_cell_number):
    data = load_data(algo, frozen_cell_number)
    return f"{algo}", min(data), st.median(data), max(data), np.average(data), np.std(data)

def get_ttest_value(algo, frozen_cell_number):
    original_data = load_data(f"original_{algo}", frozen_cell_number)
    cell_view_data = load_cell_view_data(algo, frozen_cell_number)
    ttest = stats.ttest_ind(original_data, cell_view_data, equal_var=True)
    return f"{algo}", ttest.statistic, ttest.pvalue

def get_ttest_value_for_same_algo(algo):
    original_data = load_cell_view_data(algo, 3)
    cell_view_data = load_cell_view_data(algo, 0)
    ttest = stats.ttest_ind(original_data, cell_view_data, equal_var=True)
    return f"{algo}", ttest.statistic, ttest.pvalue


def plot_bar_chart_for_diff_frozen_cells(index, traditional_df, cell_df):
    # plt.xlabel('frozen cell number')
    barWidth = 0.25
    
    # set height of bar
    traditional = [traditional_df['Avg'][index*4], traditional_df['Avg'][index*4 + 1], traditional_df['Avg'][index*4 + 2], traditional_df['Avg'][index*4 + 3]]
    cell_view = [cell_df['Avg'][index*4], cell_df['Avg'][index*4 + 1], cell_df['Avg'][index*4 + 2], cell_df['Avg'][index*4 + 3]]
    
    traditional_std = [traditional_df['Std dev'][index*4], traditional_df['Std dev'][index*4 + 1], traditional_df['Std dev'][index*4 + 2], traditional_df['Std dev'][index*4 + 3]]
    cell_view_std = [cell_df['Std dev'][index*4], cell_df['Std dev'][index*4 + 1], cell_df['Std dev'][index*4 + 2], cell_df['Std dev'][index*4 + 3]]
    
    # Set position of bar on X axisy
    br1 = np.arange(len(traditional))
    br2 = [x + barWidth for x in br1]
    
    # Make the plot
    no_frozen_bars = plt.bar(br1, traditional, color ='r', width = barWidth,
            edgecolor ='grey', label ='Traditional', yerr=traditional_std)
    one_frozen_bars = plt.bar(br2, cell_view, color ='g', width = barWidth,
            edgecolor ='grey', label ='Cell View', yerr=cell_view_std)
    
    for bar in no_frozen_bars:
        yval = round(bar.get_height(), 2)
        plt.text(bar.get_x() + barWidth / 2 , yval + .005, yval)
        
    for bar in one_frozen_bars:
        yval = round(bar.get_height(), 2)
        plt.text(bar.get_x() + barWidth / 2, yval + .005, yval)
    
    # Adding Xticks
    # plt.xlabel('Sorting Algorithm', fontweight ='bold', fontsize = 15)

    plt.xticks([r + barWidth / 2 for r in range(len(traditional))],
            ['f = 0', 'f = 1', 'f = 2', 'f = 3'], fontsize = 15)
    
    algo_name = cell_df['Sorting algorithm'][index*4].replace('_', ' ').lower()
    plt.title('Delayed gratification traditional vs cell view ' + r"$\bf{" + str(algo_name.split(" ")[0]) + "}$ " + r"$\bf{" + str(algo_name.split(" ")[1]) + "}$", )
    
    plt.ylim(ymin=0,)
    plt.legend()
    # plt.savefig(f"/Users/tainingzhang/Desktop/research_images/claim_images/cell_traditional_efficiency_comparison.png")


def plot_bar_chart_for_frozen_affect(index, traditional_df, cell_df):
    # plt.xlabel('frozen cell number')
    barWidth = 0.25
    
    # set height of bar
    traditional = [traditional_df['Avg'][index*4], traditional_df['Avg'][index*4 + 1], traditional_df['Avg'][index*4 + 2], traditional_df['Avg'][index*4 + 3]]
    cell_view = [cell_df['Avg'][index*4], cell_df['Avg'][index*4 + 1], cell_df['Avg'][index*4 + 2], cell_df['Avg'][index*4 + 3]]
    
    traditional_std = [traditional_df['Std dev'][index*4], traditional_df['Std dev'][index*4 + 1], traditional_df['Std dev'][index*4 + 2], traditional_df['Std dev'][index*4 + 3]]
    cell_view_std = [cell_df['Std dev'][index*4], cell_df['Std dev'][index*4 + 1], cell_df['Std dev'][index*4 + 2], cell_df['Std dev'][index*4 + 3]]
    
    # Set position of bar on X axisy
    br1 = np.arange(len(traditional))
    br2 = [x + barWidth for x in br1]
    
    # Make the plot
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(traditional)
    print(cell_view)
    no_frozen_bars = plt.bar(br1, traditional, color ='r', width = barWidth,
            edgecolor ='grey', label ='Traditional', yerr=traditional_std)
    one_frozen_bars = plt.bar(br2, cell_view, color ='g', width = barWidth,
            edgecolor ='grey', label ='Cell View', yerr=cell_view_std)
    
    for bar in no_frozen_bars:
        yval = round(bar.get_height(), 2)
        plt.text(bar.get_x() + barWidth / 2 , yval + .005, yval)
        
    for bar in one_frozen_bars:
        yval = round(bar.get_height(), 2)
        plt.text(bar.get_x() + barWidth / 2, yval + .005, yval)
    
    # Adding Xticks
    # plt.xlabel('Sorting Algorithm', fontweight ='bold', fontsize = 15)

    plt.xticks([r + barWidth / 2 for r in range(len(traditional))],
            ['f = 0', 'f = 1', 'f = 2', 'f = 3'], fontsize = 15)
    
    algo_name = cell_df['Sorting algorithm'][index*4].replace('_', ' ').lower()
    plt.title('Delayed gratification traditional vs cell view ' + r"$\bf{" + str(algo_name.split(" ")[0]) + "}$ " + r"$\bf{" + str(algo_name.split(" ")[1]) + "}$", )
    
    plt.ylim(ymin=0,)
    plt.legend()
    # plt.savefig(f"/Users/tainingzhang/Desktop/research_images/claim_images/cell_traditional_efficiency_comparison.png")


data = pd.DataFrame(
    [
        fetch_data_to_display('original_bubble_sort', 0),
        fetch_data_to_display('original_bubble_sort', 1),
        fetch_data_to_display('original_bubble_sort', 2),
        fetch_data_to_display('original_bubble_sort', 3),
        fetch_data_to_display('original_insertion_sort', 0),
        fetch_data_to_display('original_insertion_sort', 1),
        fetch_data_to_display('original_insertion_sort', 2),
        fetch_data_to_display('original_insertion_sort', 3),
        fetch_data_to_display('original_selection_sort', 0),
        fetch_data_to_display('original_selection_sort', 1),
        fetch_data_to_display('original_selection_sort', 2),
        fetch_data_to_display('original_selection_sort', 3),
    ], columns = ['Sorting algorithm', 'Min', 'Median', 'Max', 'Avg', 'Std dev'])
ob0_data = load_data('original_bubble_sort', 0)

ob1_data = load_data('original_bubble_sort', 1)
ob2_data = load_data('original_bubble_sort', 2)
ob3_data = load_data('original_bubble_sort', 3)
oi0_data = load_data('original_insertion_sort', 0)
oi1_data = load_data('original_insertion_sort', 1)
oi2_data = load_data('original_insertion_sort', 2)
oi3_data = load_data('original_insertion_sort', 3)
os0_data = load_data('original_selection_sort', 0)
os1_data = load_data('original_selection_sort', 1)
os2_data = load_data('original_selection_sort', 2)
os3_data = load_data('original_selection_sort', 3)
cb0_data = load_cell_view_data('bubble_sort', 0)
cb1_data = load_cell_view_data('bubble_sort', 1)
cb2_data = load_cell_view_data('bubble_sort', 2)
cb3_data = load_cell_view_data('bubble_sort', 3)
ci0_data = load_cell_view_data('insertion_sort', 0)
ci1_data = load_cell_view_data('insertion_sort', 1)
ci2_data = load_cell_view_data('insertion_sort', 2)
ci3_data = load_cell_view_data('insertion_sort', 3)
cs0_data = load_cell_view_data('selection_sort', 0)
cs1_data = load_cell_view_data('selection_sort', 1)
cs2_data = load_cell_view_data('selection_sort', 2)
cs3_data = load_cell_view_data('selection_sort', 3)

print(oi3_data)
ztest_cb_ob = ztest(cb0_data + cb1_data + cb2_data + cb3_data, ob0_data + ob1_data + ob2_data + ob3_data)
ztest_ci_oi = ztest(ci0_data + ci1_data + ci2_data + ci3_data, oi0_data + oi1_data + oi2_data + oi3_data)
ztest_cs_os = ztest(cs0_data + cs1_data + cs2_data + cs3_data, os0_data + os1_data + os2_data + os3_data)

ztest_cs_ci = ztest(cs0_data + cs1_data + cs2_data + cs3_data, ci0_data + ci1_data + ci2_data + ci3_data)
ztest_ci_cb = ztest(ci0_data + ci1_data + ci2_data + ci3_data, cb0_data + cb1_data + cb2_data + cb3_data)

print("cb ob")
print(ztest_cb_ob)
print("ci oi")
print(ztest_ci_oi)
print("cs os")
print(ztest_cs_os)


print("cs ci")
print(ztest_cs_ci)
print("ci cb")
print(ztest_ci_cb)
# print(data)

cell_view_data = pd.DataFrame(
    [
        fetch_cell_view_data_to_display('bubble_sort', 0),
        fetch_cell_view_data_to_display('bubble_sort', 1),
        fetch_cell_view_data_to_display('bubble_sort', 2),
        fetch_cell_view_data_to_display('bubble_sort', 3),
        fetch_cell_view_data_to_display('insertion_sort', 0),
        fetch_cell_view_data_to_display('insertion_sort', 1),
        fetch_cell_view_data_to_display('insertion_sort', 2),
        fetch_cell_view_data_to_display('insertion_sort', 3),
        fetch_cell_view_data_to_display('selection_sort', 0),
        fetch_cell_view_data_to_display('selection_sort', 1),
        fetch_cell_view_data_to_display('selection_sort', 2),
        fetch_cell_view_data_to_display('selection_sort', 3),
    ], columns = ['Sorting algorithm', 'Min', 'Median', 'Max', 'Avg', 'Std dev'])

fig = plt.figure(figsize = (20, 8))
fig.supylabel('monocity error')

for i in range(3):
    plt.subplot(1, 3, i + 1)
    if i == 0:
        plt.ylabel(f'Delayed Gratification', fontweight ='bold', fontsize = 15)
    plot_bar_chart_for_frozen_affect(i, data, cell_view_data)
    
    if i == 1:
        plt.xlabel('frozen cell number', fontweight ='bold', fontsize = 15)
    
plt.show()

# print(cell_view_data)

# ttest_data = pd.DataFrame(
#     [
#         get_ttest_value('bubble_sort', 0),
#         get_ttest_value('bubble_sort', 1),
#         get_ttest_value('bubble_sort', 2),
#         get_ttest_value('bubble_sort', 3),
#         get_ttest_value('insertion_sort', 0),
#         get_ttest_value('insertion_sort', 1),
#         get_ttest_value('insertion_sort', 2),
#         get_ttest_value('insertion_sort', 3),
#         get_ttest_value('selection_sort', 0),
#         get_ttest_value('selection_sort', 1),
#         get_ttest_value('selection_sort', 2),
#         get_ttest_value('selection_sort', 3),
#     ], columns = ['Sorting algorithm', 'ttest statistic', 'ttest pvalue'])

# print(ttest_data)


ttest_data_for_frozen_cells = pd.DataFrame(
    [
        get_ttest_value_for_same_algo('bubble_sort'),
        get_ttest_value_for_same_algo('insertion_sort'),
        get_ttest_value_for_same_algo('selection_sort'),
    ], columns = ['Sorting algorithm', 'ttest statistic', 'ttest pvalue'])

print(ttest_data_for_frozen_cells)