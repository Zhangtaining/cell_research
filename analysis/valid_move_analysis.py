from performance_analysis import (
    get_original_exp_monotonicities,
    get_cell_exp_monotonicities,
    get_original_algo_sorting_file_path,
    get_cell_algo_sorting_file_path
)
import matplotlib.pyplot as plt
import random

def valid_steps(arr):
    res = []
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            res.append(i) 
    return res

def valid_steps_in_each_experiment(arr):
    return [valid_steps(a) for a in arr]

def plot_valid_step_distribution(algo, frozen_cell, is_original=False):
    monotonicity_list = []
    if is_original:
        monotonicity_list = get_original_exp_monotonicities(get_original_algo_sorting_file_path(algo, frozen_cell))
    else:
        monotonicity_list = get_cell_exp_monotonicities(get_cell_algo_sorting_file_path(algo, frozen_cell))
    v_steps_exps = valid_steps_in_each_experiment(monotonicity_list)
    r = random.randint(0, len(v_steps_exps)-1)
    v_steps = v_steps_exps[r]
    c = random.random()
    y = [1 for i in range(len(v_steps))]
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle(f"{' origin' if is_original else ''} {algo} with {frozen_cell} frozen cells")
    ax1.plot([n for n in range(len(monotonicity_list[r]))], monotonicity_list[r])
    ax1.set_title(f"Monotonicity Change")
    ax2.scatter(v_steps, y, s=50, alpha=0.2)
    ax2.set_yticks([])
    ax2.set_ylabel('valid steps')
    ax2.set_xlabel('steps')
    ax2.set_title("Valid Step Distribution")
    plt.show()

for algo in ['step_selection']:
    for frozen_cell in range(3):
        plot_valid_step_distribution(algo, frozen_cell, True)
        # plot_valid_step_distribution(algo, frozen_cell, False)

