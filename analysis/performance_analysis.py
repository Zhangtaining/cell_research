import numpy as np
from utils import get_monotonicity
import scipy.stats as stats
import pandas as pd


def get_final_monotonicity(arr):
    return arr[-1]

def get_steps_to_reach_final_monotonicity(arr):
    return  arr.index(arr[-1])

def get_avg_final_monotonicity(arr):
    return  np.average([get_final_monotonicity(a) for a in arr])

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

def get_original_algo_sorting_file_path(algo, frozen_cells):
    return f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_{algo}_sort_with_{frozen_cells}frozen_cannot_move_sorting_steps_100exps.npy"

def get_cell_algo_sorting_file_path(algo, frozen_cells):
    return f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{algo}_sort_sorting_with_{frozen_cells}frozen_cannot_move_steps_100exps.npy"


def compare_algorithms(algo, frozen_cells):
    original_file = get_original_algo_sorting_file_path(algo, frozen_cells)
    cell_file = get_cell_algo_sorting_file_path(algo, frozen_cells)
    original_exp_monotonicities = get_original_exp_monotonicities(original_file)
    cell_exp_monotonicities = get_cell_exp_monotonicities(cell_file)
    print(f"avg final monotonicity: {get_avg_final_monotonicity(original_exp_monotonicities)}, {get_avg_final_monotonicity(cell_exp_monotonicities)}, {stats.ttest_ind([get_final_monotonicity(a) for a in original_exp_monotonicities], [get_final_monotonicity(a) for a in cell_exp_monotonicities], equal_var=True)}")
    print(f"avg steps to final monotonicity: {get_avg_steps_to_reach_final_monotonicity(original_exp_monotonicities)}, {get_avg_steps_to_reach_final_monotonicity(cell_exp_monotonicities)}, {stats.ttest_ind([get_steps_to_reach_final_monotonicity(a) for a in original_exp_monotonicities], [get_steps_to_reach_final_monotonicity(a) for a in cell_exp_monotonicities], equal_var=True)}")

def get_observe_matrix(algo):
    return [[get_final_monotonicity(a) for a in get_cell_exp_monotonicities(get_cell_algo_sorting_file_path(algo, f))] for f in range(1, 4)]

for f in range(1, 4):
    compare_algorithms('selection', f)

# df = pd.DataFrame(get_observe_matrix('selection'))
# print(df)

# print(stats.chi2_contingency(df))