import numpy as np
from utils import get_monotonicity
import scipy.stats as stats
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.weightstats import ztest as ztest


def get_final_monotonicity(arr):

    return 100 - arr[-1]

def get_final_success_value(arr):
    return 1 if arr[-1] == 0 else 0

def get_steps_to_reach_final_monotonicity(arr):
    return  arr.index(arr[-1])

def get_avg_final_monotonicity(arr):
    return  np.average([get_final_monotonicity(a) for a in arr if len(a) > 0])

def get_avg_steps_to_reach_final_monotonicity(arr):
    return np.average([get_steps_to_reach_final_monotonicity(a) for a in arr])

def get_monotonicity_arr(arr):
    return [get_monotonicity(step) for step in arr if len(step) > 0]

def get_cell_exp_monotonicities(file):
    experiments = np.load(file, allow_pickle=True)
    return [get_monotonicity_arr(exp_record) for exp_record in experiments ]

def get_original_exp_monotonicities(file):
    experiments = np.load(file, allow_pickle=True,)
    return [exp_record for exp_record in experiments]

def get_original_algo_sorting_file_path(algo, frozen_cells, movable=True):
    # if movable:
    #     return f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_{algo}_sort_sorting_with_{frozen_cells}frozen_frozen_swap_count_100exps.npy"
    return f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_{algo}_sort_with_{frozen_cells}frozen_cannot_move_sorting_steps_100exps.npy"

def get_cell_algo_sorting_file_path(algo, frozen_cells, movable=True):
    if movable:
        return f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{algo}_sort_sorting_with_{frozen_cells}frozen_steps_100exps.npy"
    return f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{algo}_sort_sorting_with_{frozen_cells}frozen_cannot_move_steps_100exps.npy"

def get_frozen_cell_distance(cell_types, frozen_number):
    first_index = cell_types.index(1)
    i = first_index + 1
    prev = first_index
    res = 0
    while i < len(cell_types):
        if cell_types[i] == 1:
            res += i-prev
            prev = i
        i+=1
    return res / (frozen_number - 1)

def plot_final_step_sorting_cell(algo, frozen_cells):
    file_name = f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{algo}_sort_sorting_with_{frozen_cells}frozen_steps_cell_type_100exps.npy"
    exps = np.load(file_name, allow_pickle=True), 
    res = []
    for exp in exps[0]:
        last_step = exp[-1]
        cell_type_in_last_step =  [c[3] for c in last_step]
        res.append(get_frozen_cell_distance(cell_type_in_last_step, frozen_cells))
    
    first_res = []
    for exp in exps[0]:
        first_step = exp[0]
        cell_type_in_last_step =  [c[3] for c in first_step]
        first_res.append(get_frozen_cell_distance(cell_type_in_last_step, frozen_cells))
        
    # print(first_res)
    # print(np.average(first_res))
    # print(np.std(first_res))
    
    # print(res)
    # print(np.average(res))
    # print(np.std(res))

def get_success_rate_for_original_exp(file):
    exps = np.load(file, allow_pickle=True)
    return [get_final_monotonicity(exp) for exp in exps]
    success_count = np.average([get_final_monotonicity(exp) for exp in exps])
    return success_count

def get_success_rate_for_cell_exp(file):
    exps = get_cell_exp_monotonicities(file)
    return [get_final_monotonicity(exp) for exp in exps if len(exp) > 0]
    success_count = np.average(([get_final_monotonicity(exp) for exp in exps if len(exp) > 0]))
    #success_count = np.average(([exp[-1] for exp in exps if exp]))
    return success_count


# def plot_bar_chart_for_frozen_affect_to_cell():
#     success_results_0_frozen_bubble =  get_success_rate_for_cell_exp(get_cell_algo_sorting_file_path('bubble', 0))
#     success_results_1_frozen_bubble = get_success_rate_for_cell_exp(get_cell_algo_sorting_file_path('bubble', 1))
#     success_results_0_frozen_insertion = get_success_rate_for_cell_exp(get_cell_algo_sorting_file_path('insertion', 0))
#     success_results_1_frozen_insertion = get_success_rate_for_cell_exp(get_cell_algo_sorting_file_path('insertion', 1))
#     success_results_0_frozen_selection = get_success_rate_for_cell_exp(get_cell_algo_sorting_file_path('selection', 0))
#     success_results_1_frozen_selection = get_success_rate_for_cell_exp(get_cell_algo_sorting_file_path('selection', 1))
    
#     barWidth = 0.25
#     # plt.figure(figsize =(12, 8))
    
#     # set height of bar
#     no_frozen = [success_results_0_frozen_bubble, success_results_0_frozen_insertion, success_results_0_frozen_selection]
#     one_frozen = [success_results_1_frozen_bubble, success_results_1_frozen_insertion, success_results_1_frozen_selection]
    
#     # Set position of bar on X axis
#     br1 = np.arange(len(no_frozen))
#     br2 = [x + barWidth for x in br1]
    
#     # Make the plot
#     no_frozen_bars = plt.bar(br1, no_frozen, color ='r', width = barWidth,
#             edgecolor ='grey', label ='No Frozen Cell')
#     one_frozen_bars = plt.bar(br2, one_frozen, color ='g', width = barWidth,
#             edgecolor ='grey', label ='One Frozen Cell')
    
#     for bar in no_frozen_bars:
#         yval = bar.get_height()
#         plt.text(bar.get_x() + barWidth / 2 , yval + .005, yval)
        
#     for bar in one_frozen_bars:
#         yval = bar.get_height()
#         plt.text(bar.get_x() + barWidth / 2, yval + .005, yval)
    
#     # Adding Xticks
#     # plt.xlabel('Sorting Algorithm', fontweight ='bold', fontsize = 15)
#     plt.ylabel('Monotonicity Error', fontweight ='bold', fontsize = 15)
#     plt.xticks([r + barWidth / 2 for r in range(len(no_frozen))],
#             ['bubble', 'insertion', 'selection'], fontsize = 18)
    
#     plt.title(f'Frozen Cell Impact to Cell View Sorting Algorithms')
    
#     plt.legend()
#     # plt.savefig(f"/Users/tainingzhang/Desktop/research_images/claim_images/cell_traditional_efficiency_comparison.png")


def plot_bar_chart_for_frozen_affect(fozen_cell_number, movable=False):
    success_results_bubble_arr = get_success_rate_for_original_exp(get_original_algo_sorting_file_path('bubble', fozen_cell_number, movable=movable))
    success_results_cell_bubble_arr = get_success_rate_for_cell_exp(get_cell_algo_sorting_file_path('bubble', fozen_cell_number, movable=movable))
    success_results_insertion_arr = get_success_rate_for_original_exp(get_original_algo_sorting_file_path('insertion', fozen_cell_number, movable=movable))
    success_results_cell_insertion_arr = get_success_rate_for_cell_exp(get_cell_algo_sorting_file_path('insertion', fozen_cell_number, movable=movable))
    success_results_selection_arr = get_success_rate_for_original_exp(get_original_algo_sorting_file_path('selection', fozen_cell_number, movable=movable))
    success_results_cell_selection_arr = get_success_rate_for_cell_exp(get_cell_algo_sorting_file_path('selection', fozen_cell_number, movable=movable))
    success_results_bubble = np.average(success_results_bubble_arr)
    success_results_cell_bubble = np.average(success_results_cell_bubble_arr)
    success_results_insertion = np.average(success_results_insertion_arr)
    success_results_cell_insertion = np.average(success_results_cell_insertion_arr)
    success_results_selection = np.average(success_results_selection_arr)
    success_results_cell_selection = np.average(success_results_cell_selection_arr)
    print(f">>>>>>>>>>>>>>>>>>>>fozen cell {fozen_cell_number}>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(f"average bubble: {success_results_bubble} std bubble: {np.std(success_results_bubble_arr)}")
    print(f"average cell bubble: {success_results_cell_bubble} std cell bubble: {np.std(success_results_cell_bubble_arr)}")
    print(f"average insertion: {success_results_insertion} std insertion: {np.std(success_results_insertion_arr)}")
    print(f"average cell insertion: {success_results_cell_insertion} std cell insertion: {np.std(success_results_cell_insertion_arr)}")
    print(f"average selection: {success_results_selection} std selection: {np.std(success_results_selection_arr)}")
    print(f"average cell selection: {success_results_cell_selection} std cell_selection: {np.std(success_results_cell_selection_arr)}")
    # ztest_bubble = ztest(success_results_cell_bubble_arr, success_results_bubble_arr)
    # ztest_insertion =  ztest(success_results_cell_insertion_arr, success_results_insertion_arr)
    # ztest_selection = ztest(success_results_cell_selection_arr, success_results_selection_arr)
    # print("bubble")
    # print(ztest_bubble)
    # print("insertion")
    # print(ztest_insertion)
    # print("selection")
    # print(ztest_selection)
    
    # ztest_bubble_selection = ztest(success_results_cell_bubble_arr, success_results_cell_selection_arr)
    # ztest_bubble_insertion =  ztest(success_results_cell_bubble_arr, success_results_cell_insertion_arr)
    # print("bubble_selection")
    # print(ztest_bubble_selection)
    # print("bubble_insertion")
    # print(ztest_bubble_insertion)
    
    barWidth = 0.25
    
    # set height of bar
    traditional = [success_results_bubble, success_results_insertion, success_results_selection]
    cell_view = [success_results_cell_bubble, success_results_cell_insertion, success_results_cell_selection]
    
    # Set position of bar on X axis
    br1 = np.arange(len(traditional))
    br2 = [x + barWidth for x in br1]
    
    # Make the plot
    no_frozen_bars = plt.bar(br1, traditional, color ='r', width = barWidth,
            edgecolor ='grey', label ='Tradition')
    one_frozen_bars = plt.bar(br2, cell_view, color ='g', width = barWidth,
            edgecolor ='grey', label ='Cell View')
    
    for bar in no_frozen_bars:
        yval = round(bar.get_height(), 2)
        plt.text(bar.get_x() + barWidth / 2 , yval + .005, yval)
        
    for bar in one_frozen_bars:
        yval = round(bar.get_height(), 2)
        plt.text(bar.get_x() + barWidth / 2, yval + .005, yval)
    
    # Adding Xticks
    # plt.xlabel('Sorting Algorithm', fontweight ='bold', fontsize = 15)
    plt.ylabel(f'frozen cell = {fozen_cell_number}')
    plt.xticks([r + barWidth / 2 for r in range(len(traditional))],
            ['bubble', 'insertion', 'selection'], fontsize = 15)
    
    # plt.title(f'Frozen Cell Impact to Traditional and Cell View Sorting Algorithms')
    
    plt.legend()
    # plt.savefig(f"/Users/tainingzhang/Desktop/research_images/claim_images/cell_traditional_efficiency_comparison.png")


def compare_algorithms(algo, frozen_cells):
    original_file = get_original_algo_sorting_file_path(algo, frozen_cells)
    cell_file = get_cell_algo_sorting_file_path(algo, frozen_cells)
    original_exp_monotonicities = get_original_exp_monotonicities(original_file)
    cell_exp_monotonicities = get_cell_exp_monotonicities(cell_file)
    print(f"avg final monotonicity: {get_avg_final_monotonicity(original_exp_monotonicities)}, {get_avg_final_monotonicity(cell_exp_monotonicities)}, {stats.ttest_ind([get_final_monotonicity(a) for a in original_exp_monotonicities], [get_final_monotonicity(a) for a in cell_exp_monotonicities], equal_var=True)}")
    print(f"avg steps to final monotonicity: {get_avg_steps_to_reach_final_monotonicity(original_exp_monotonicities)}, {get_avg_steps_to_reach_final_monotonicity(cell_exp_monotonicities)}, {stats.ttest_ind([get_steps_to_reach_final_monotonicity(a) for a in original_exp_monotonicities], [get_steps_to_reach_final_monotonicity(a) for a in cell_exp_monotonicities], equal_var=True)}")

def get_observe_matrix(algo):
    return [[get_final_monotonicity(a) for a in get_cell_exp_monotonicities(get_cell_algo_sorting_file_path(algo, f))] for f in range(1, 4)]

# for f in range(1, 4):
#     compare_algorithms('selection', f)
def plot_all_unmovable_graph():
    figure = plt.figure(figsize =(8, 12))
    figure.supylabel('Monotonicity Error', fontweight ='bold', fontsize = 15)
    figure.suptitle("Frozen Cell Unmovable by Others")
    plt.subplot(3, 1, 1)
    plot_bar_chart_for_frozen_affect(1)
    plt.title('Traditional vs Cell View Algorithms', fontweight ='bold', fontsize = 15)

    plt.subplot(3, 1, 2)
    plot_bar_chart_for_frozen_affect(2)

    plt.subplot(3, 1, 3)
    plot_bar_chart_for_frozen_affect(3)

    # plt.show()
plot_all_unmovable_graph()

#plot_final_step_sorting_cell('bubble', 2)
    
def plot_all_movable_graph():
    figure = plt.figure(figsize =(8, 12))
    figure.supylabel('Monotonicity Error', fontweight ='bold', fontsize = 15)
    figure.suptitle("Frozen Cell Movable by Others")
    plt.subplot(3, 1, 1)
    plot_bar_chart_for_frozen_affect(1, True)
    plt.title('Traditional vs Cell View Algorithms', fontweight ='bold', fontsize = 15)

    plt.subplot(3, 1, 2)
    plot_bar_chart_for_frozen_affect(2, True)

    plt.subplot(3, 1, 3)
    plot_bar_chart_for_frozen_affect(3, True)

    # plt.show()
plot_all_movable_graph()

# df = pd.DataFrame(get_observe_matrix('selection'))
# print(df)

# print(stats.chi2_contingency(df))