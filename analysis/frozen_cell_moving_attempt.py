import numpy as np

def get_cell_algo_sorting_file_path(algo, frozen_cells):
    return f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{algo}_sort_sorting_with_{frozen_cells}frozen_cannot_move_steps_100exps.npy"

def get_frozen_cell_attempt_file_path(algo, frozen_cells):
    return f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{algo}_sort_sorting_with_{frozen_cells}frozen_frozen_swap_count_100exps.npy"

def get_original_algo_sorting_file_path(algo, frozen_cells):
    return f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_{algo}_sort_with_{frozen_cells}frozen_cannot_move_sorting_steps_100exps.npy"

def get_original_frozen_cell_attempt_file_path(algo, frozen_cells):
    return f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_{algo}_sort_sorting_with_{frozen_cells}frozen_frozen_swap_count_100exps.npy"

def get_avg_total_steps(file):
    exps = np.load(file, allow_pickle=True)
    return np.average([len(exp) for exp in exps])

def get_avg_frozen_cell_attempt(file):
    exps = np.load(file, allow_pickle=True)
    return np.average([attempt for attempt in exps])

def get_frozen_cell_attempt_stats():
    for algo in ['bubble', 'insertion', 'selection']:
        for frozen_cells in range(4):
            print(f"{algo} with {frozen_cells} frozen cells: {get_avg_frozen_cell_attempt(get_frozen_cell_attempt_file_path(algo, frozen_cells))}, {get_avg_total_steps(get_cell_algo_sorting_file_path(algo, frozen_cells))}")

def get_original_frozen_cell_attempt_stats():
    for algo in ['bubble', 'insertion', 'selection']:
        for frozen_cells in range(4):
            print(f"{algo} with {frozen_cells} frozen cells: {get_avg_frozen_cell_attempt(get_original_frozen_cell_attempt_file_path(algo, frozen_cells))}, {get_avg_total_steps(get_original_algo_sorting_file_path(algo, frozen_cells))}")


get_frozen_cell_attempt_stats()
get_original_frozen_cell_attempt_stats()
