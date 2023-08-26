import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.patheffects import PathPatchEffect, SimpleLineShadow, Normal, Stroke
from scipy import stats
import seaborn as sns
from scipy.optimize import curve_fit
import scipy.stats as stats
import pandas as pd
import random

# moves = np.load('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/cell_type_with_group_id_evenly_dist.npy')
def get_value_cell_type_map(arr):
    value_map = {}
    for [_, cell_type, value] in arr:
        if value not in value_map:
            value_map[value] = []
        group_steps = value_map[value]
        group_steps.append(cell_type)
    return value_map

def get_ttest_value(arr1, arr2):
    return stats.ttest_ind(arr1, arr2, equal_var=True)

# def update_cell_type_map(overall_map, c_map):
#     for key in c_map:
#         if key in overall_map:
#             if not same_step(overall_map[key][-1], c_map[key]):
#                 overall_map[key].append(c_map[key])
#         else:
#             overall_map[key] = [c_map[key]]

# def same_step(arr1, arr2):
#     if len(arr1) != len(arr2):
#         return False 
    
#     for i in range(len(arr1)):
#         if arr1[i] != arr2[i]:
#             return False 
    
#     return True
def get_aggregation_score(cell_types):
    counting_map = {}
    prev_ct = cell_types[0]
    consecutive_cnt = 0
    # print(cell_types)
    for ct in cell_types[1:]:
        if ct == prev_ct:
            consecutive_cnt += 1
        else:
            counting_map[prev_ct] = max(counting_map.get(prev_ct, 0), consecutive_cnt)
            consecutive_cnt = 0
            prev_ct = ct
    result = sum([v for v in counting_map.values()])
    # print(result)
    return result


def get_aggregation_score_map(value_map):
    aggregation_score_map = {}
    for key, cell_types in value_map.items():
        aggregation_score_map[key] = get_aggregation_score(cell_types)
    return aggregation_score_map


def trim_the_list(homogenity_list):
    res = []
    for l in homogenity_list:
        if len(res) == 0 or len(l) != len(res[-1]):
            res.append(l)
    return res





# def process_moves(moves):
#     overall_map = {}
#     for move in moves:
#         c_map = get_cell_type_in_each_group(move)
#         update_cell_type_map(overall_map, c_map)
#     return overall_map
    
# overall_map = process_moves(moves)
# print(overall_map)

# homogenity_at_each_move = trim_the_list([get_homogenity_in_each_group(move) for move in moves])



# x = [n for n in range(len(homogenity_at_each_move))]

# max_homogenity_at_each_move = [max(homogenity) for homogenity in homogenity_at_each_move]
# avg_homogenity_at_each_move = [np.average(homogenity) for homogenity in homogenity_at_each_move]
# avg_add_std_homogenity_at_each_move = [np.std(homogenity) + np.average(homogenity) for homogenity in homogenity_at_each_move]
# avg_minus_std_homogenity_at_each_move = [np.average(homogenity) - np.std(homogenity) for homogenity in homogenity_at_each_move]

# plt.figure()
# plt.xlabel('group merge')
# plt.ylabel('homogenity')
# plt.plot(x, max_homogenity_at_each_move, color='r', label="max homogenity",)
# plt.plot(x, avg_homogenity_at_each_move, color='b', label="avg homogenity",)
# plt.fill_between(x, avg_minus_std_homogenity_at_each_move, avg_add_std_homogenity_at_each_move, color='g', alpha=0.1)
# plt.legend(loc='best')
# plt.show()

def process_each_move(move, max_aggregation_score_map):
    value_map = get_value_cell_type_map(move)
    aggregation_score_map = get_aggregation_score_map(value_map)
    for key in aggregation_score_map:
        max_aggregation_score_map[key] = max(max_aggregation_score_map.get(key, 0), aggregation_score_map[key])
        

def build_neighbor_checking_arr(move):
    res = []
    for i in range(len(move)):
        has_same_neighbor = False
        # left = i -1
        # if left >= 0:
        #     has_same_neighbor = has_same_neighbor or (move[left][1] == move[i][1])
        
        right = i + 1
        if right < len(move):
            has_same_neighbor = has_same_neighbor or (move[right][1] == move[i][1])
        
        if has_same_neighbor:
            res.append(1)
        else:
            res.append(0)
    return res

def get_aggregation_value_avg(move):
    return np.average(build_neighbor_checking_arr(move))


def get_aggregation_value(move):
    rand_index = random.randint(1, len(move) - 2)
    left = rand_index - 1
    right = rand_index + 1
    res = 0
    if move[rand_index][1] == move[left][1]:
        res += 0.5
    if move[rand_index][1] == move[right][1]:
        res += 0.5
    return res

def get_monotonicity_value(move):
    arr = [m[2] for m in move]
    monotonicity_value = 0
    prev = arr[0]
    for i in range(1, len(arr)):
        if arr[i] >= prev:
            monotonicity_value += 1
        prev = arr[i]
    return monotonicity_value


def get_monotonicity_value_for_cell_type(move, cell_type):
    arr = [m[2] for m in move if m[1] == cell_type]
    if not arr:
        return -1
    monotonicity_value = 0
    prev = arr[0]
    for i in range(1, len(arr)):
        if arr[i] >= prev:
            monotonicity_value += 1
        prev = arr[i]
    return monotonicity_value

def cell_type_moved(cell_type, previous_move, current_move):
    prev_cell_position_map = [i for i in range(len(previous_move)) if previous_move[i][1] == cell_type]
    current_cell_position_map = [i for i in range(len(current_move)) if current_move[i][1] == cell_type]
    for i in range(len(current_cell_position_map)):
        if current_cell_position_map[i] - prev_cell_position_map[i] < 0:
            return True
    return False

def get_monotonicity_value_for_other_cell_moves(move, cell_type):
    arr = [m[2] for m in move if m[1] == cell_type]
    if not arr:
        return -1
    monotonicity_value = 0
    prev = arr[0]
    for i in range(1, len(arr)):
        if arr[i] >= prev:
            monotonicity_value += 1
        prev = arr[i]
    return monotonicity_value


def get_monotonicity_array_for_other_cell_move(exps, cell_type, other_cell_type):
    monotonicity_arr = []
    moves = exps[random.randint(0, len(exps))]
    for i in range(1, len(moves)):
        if cell_type_moved(other_cell_type, moves[i - 1], moves[i]):
            monotonicity_arr.append(get_monotonicity_value_for_cell_type(moves[i], cell_type))
    return monotonicity_arr


def plot_aggregation_value(moves):
    aggregation_value_list = [get_aggregation_value_avg(m) for m in moves]
    x = [n for n in range(len(aggregation_value_list))]
    plt.plot(x, aggregation_value_list)
    

def plot_moves_file(dir, title):
    plt.figure()
    plt.xlabel('sorting steps')
    plt.ylabel('aggregation value')
    plt.title(title)
    for i in range(1):
        moves = np.load(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{dir}/exp_{i}.npy")
        plot_aggregation_value(moves)
    file_name = title.replace(" ", "_").lower()
    plt.savefig(f"/Users/tainingzhang/Desktop/research_images/claim_images/{file_name}.png")
    plt.show()


def get_step_at_pct(moves, p):
    idx = int((len(moves) - 1) * p)
    return moves[idx]

    
def get_average_aggregation_array(exps, factor=1):
    avg_res = []
    std_up_res = []
    std_down_res = []
    for i in range(101):
        p = (i * factor) / 100
        p = min(p, 1)
        aggregation_values = [get_aggregation_value_avg(get_step_at_pct(moves, p)) for moves in exps]
        avg_res.append(np.average(aggregation_values))
        std_up_res.append(np.std(aggregation_values) + np.average(aggregation_values))
        std_down_res.append(-np.std(aggregation_values) + np.average(aggregation_values))
    return avg_res, std_up_res, std_down_res

def get_average_monotonicity_array_for_cell_type(exps, cell_type):
    avg_res = []
    std_up_res = []
    std_down_res = []
    for i in range(101):
        p = i / 100
        monotonicity_values = [get_monotonicity_value_for_cell_type(get_step_at_pct(moves, p), cell_type) for moves in exps if get_monotonicity_value_for_cell_type(get_step_at_pct(moves, p), cell_type) != -1]
        if monotonicity_values:
            avg_res.append(np.average(monotonicity_values))
            std_up_res.append(np.average(monotonicity_values) + np.std(monotonicity_values))
            std_down_res.append(np.average(monotonicity_values) - np.std(monotonicity_values))
    return avg_res, std_up_res, std_down_res

def get_average_monotonicy_array(exps, factor=1):
    avg_res = []
    std_up_res = []
    std_down_res = []
    for i in range(101):
        p = (i*factor) / 100
        p = min(p, 1)
        monotonicity_values = [get_monotonicity_value(get_step_at_pct(moves, p)) for moves in exps]
        avg_res.append(np.average(monotonicity_values))
        std_up_res.append(np.average(monotonicity_values) + np.std(monotonicity_values))
        std_down_res.append(np.average(monotonicity_values) - np.std(monotonicity_values))
    return avg_res, std_up_res, std_down_res



def plot_final_sorting_results(dir, title):
    exps = [np.load(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{dir}/exp_{i}.npy", allow_pickle=True) for i in range(100)]
    last_step = [s[2] for s in exps[random.randint(0, len(exps))][-1]]
    cell_types = [s[1] for s in exps[random.randint(0, len(exps))][-1]]
    x = [n for n in range(len(last_step))]
    plt.figure()
    plt.xlabel('position')
    plt.ylabel('cell value')
    plt.title(title)
    plt.scatter(x, last_step, marker="o", c=cell_types, s=20, cmap='winter')
    plt.plot(x, last_step, color='grey')
    plt.show()

def get_max_aggregation_step(exp):
    aggregation_list = [get_aggregation_value_avg(exp[i]) for i in range(len(exp))]
    max_index = 0
    for i in range(len(aggregation_list)):
        if aggregation_list[i] > aggregation_list[max_index]:
            max_index = i
            
    return max_index

def get_cell_color(cell_type):
    color_map = ['g', 'c', 'm']
    return color_map[cell_type]


def get_cells_for_cell_type(cell_type, step):
    pos = []
    value = []
    for i in range(len(step)):
        s = step[i]
        if s[1] == cell_type:
            pos.append(i)
            value.append(s[2])
    return pos, value

def plot_max_aggregation_digits(dir, title, subgraph_pos):
    exps = [np.load(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{dir}/exp_{i}.npy", allow_pickle=True) for i in range(100)]
    exp = exps[random.randint(0, len(exps))]
    max_index = get_max_aggregation_step(exp)
    step = [s[2] for s in exp[max_index]]
    x = [n for n in range(len(step))]
    plt.subplot(subgraph_pos[0], subgraph_pos[1], subgraph_pos[2])
    plt.xlabel('position')
    plt.ylabel('cell value')
    plt.title(title)
    # find bubble points and plot
    bubble_pos, bubble_value = get_cells_for_cell_type(0, exp[max_index])
    if bubble_pos:
        plt.scatter(bubble_pos, bubble_value, marker="o", c=get_cell_color(0), s=20, label="bubble")
    
    # find insertion points and plot
    insertion_pos, insertion_value = get_cells_for_cell_type(2, exp[max_index])
    if insertion_pos:
        plt.scatter(insertion_pos, insertion_value, marker="o", c=get_cell_color(2), s=20,  label="insertion")
    
    # find selection points and plot
    selection_pos, selection_value = get_cells_for_cell_type(1, exp[max_index])
    if selection_pos:
        plt.scatter(selection_pos, selection_value, marker="o", c=get_cell_color(1), s=20, label='selection')

    plt.plot(x, step, color='grey')
    
    plt.legend(loc="upper right")
    
    
def cell_type_str_to_number(cell_type_name):
    cell_type_map = {
        'bubble': 0,
        'selection': 1,
        'insertion': 2
    }    
    return cell_type_map[cell_type_name]

def plot_cell_monotonicity_change_by_other_cell_move(dir, cell_1_name, cell_2_name, plot_shape, row):
    cell_1 = cell_type_str_to_number(cell_1_name)
    cell_2 = cell_type_str_to_number(cell_2_name)
    exps = [np.load(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{dir}/exp_{i}.npy", allow_pickle=True) for i in range(100)]
    m_arr_1 = get_monotonicity_array_for_other_cell_move(exps, cell_1, cell_2)
    m_arr_2 = get_monotonicity_array_for_other_cell_move(exps, cell_2, cell_1)
    
    # plt.figure()
    plt.subplot(plot_shape[0], plot_shape[1], 2 * row - 1)
    x = [n for n in range(len(m_arr_1))]
    plt.title(f'{cell_1_name} cell sortedness change as {cell_2_name} cell moving', fontsize = 10)
    plt.xlabel(f'{cell_2_name} cell moves')
    plt.ylabel(f'{cell_1_name} cell sortedness')
    plt.plot(x, m_arr_1)
    
    plt.subplot(plot_shape[0], plot_shape[1], 2 * row)
    plt.title(f'{cell_2_name} cell sortedness change as {cell_1_name} cell moving', fontsize = 10)
    plt.xlabel(f'{cell_1_name} cell moves')
    plt.ylabel(f'{cell_2_name} cell sortedness')
    x = [n for n in range(len(m_arr_2))]
    plt.plot(x, m_arr_2)
    
    if row == plot_shape[0]:
        plt.subplot_tool()
        plt.show()
    
def plot_dis_order(dir, title, up_cell, down_cell, plot_shape):
    exps = [np.load(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{dir}/exp_{i}.npy", allow_pickle=True) for i in range(100)]
    aggregation_value_list, aggregation_std_up, aggregation_std_down = get_average_aggregation_array(exps, factor=1.25)
    monotonicity_value_list, monotonicity_std_up, monotonicity_std_down = get_average_monotonicy_array(exps, factor=1.25)
    x = [n for n in range(len(aggregation_value_list))]
    ax1 = plt.subplot(plot_shape[0], plot_shape[1], plot_shape[2])
    color = 'tab:red'
    ax1.set_title(title)
    ax1.set_xlabel('sorting process pct(%)')
    ax1.set_ylabel('aggregation value', color=color)
    ax1.plot(x, aggregation_value_list, color=color, linewidth=3, label="aggregation value")
    ax1.fill_between(x, aggregation_std_down, aggregation_std_up, color=color, alpha=0.1)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(ymin=0.3, ymax=1)
    ax1.legend(loc="upper left")
    
    # bubble_bubble_exps = [np.load(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/cell_type_aggregation_random_dist_100_tests_bubble_bubble_bubble/exp_{i}.npy") for i in range(100)]
    # bubble_aggregation_value_list, _, _ = get_average_aggregation_array(bubble_bubble_exps)
    # ax1.plot(x, bubble_aggregation_value_list, color='pink', label="same type cells aggregation value change")
    # ax1.legend(loc="lower left")
    
    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Increasing & Decreasing Sortedness', color=color)
    ax2.plot(x, monotonicity_value_list, color=color, linewidth=3, label="sortedness")
    ax2.fill_between(x, monotonicity_std_down, monotonicity_std_up, color=color, alpha=0.1)
    ax2.tick_params(axis='y', labelcolor=color)
    # ax2.set_ylim(ymin=0, ymax=100)
    ax2.axhline(np.average(monotonicity_value_list), color='grey', linestyle='--', linewidth=0.5)
    ax2.text(90, np.average(monotonicity_value_list) + 1, up_cell, color=get_cell_color(cell_type_str_to_number(up_cell)))
    ax2.text(90, np.average(monotonicity_value_list) - 1, down_cell, color=get_cell_color(cell_type_str_to_number(down_cell)))
        
    ax2.legend(loc="upper right")
    
    print(f"max aggregation for {dir}: {max(aggregation_value_list)}, {aggregation_std_up[aggregation_value_list.index(max(aggregation_value_list))] - max(aggregation_value_list)}")
    print(f"final monotonicity for {dir}: {monotonicity_value_list[-1]}, {monotonicity_std_up[-1] - monotonicity_value_list[-1]}")

def plot_average_data_from_experiment(dir, title, plot_shape, subplot_idx=-1, three_type=False, should_split=False):
    exps = [np.load(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{dir}/exp_{i}.npy", allow_pickle=True) for i in range(20)]
    aggregation_value_list, aggregation_std_up, aggregation_std_down = get_average_aggregation_array(exps)
    monotonicity_value_list, monotonicity_std_up, monotonicity_std_down = get_average_monotonicy_array(exps)
    x = [n for n in range(len(aggregation_value_list))]
    if subplot_idx <=0:
        ax1 = plt.gca()
    else:
        ax1 = plt.subplot(plot_shape[0], plot_shape[1], subplot_idx)
    color = 'tab:red'
    ax1.set_title(title,  fontsize = 25)
    ax1.set_xlabel('sorting process pct(%)', fontsize = 25)
    ax1.set_ylabel('aggregation value', color=color,  fontsize = 25)
    ax1.plot(x, aggregation_value_list, color=color, linewidth=3, label="aggregation value change")
    ax1.fill_between(x, aggregation_std_down, aggregation_std_up, color=color, alpha=0.1)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(ymin=0.3, ymax=1)
    ax1.legend(loc="upper left")
    
    suffix = "" if not three_type else "_bubble"
    bubble_bubble_exps = [np.load(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/cell_type_aggregation_random_dist_100_tests_bubble_bubble{suffix}/exp_{i}.npy") for i in range(100)]
    bubble_aggregation_value_list, _, _ = get_average_aggregation_array(bubble_bubble_exps)
    ax1.plot(x, bubble_aggregation_value_list, color='pink', label="same type cells aggregation value change")
    ax1.legend(loc="lower left")
    
    
    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('sortedness', color=color, fontsize = 25)
    if not should_split:
        ax2.plot(x, monotonicity_value_list, color=color, linewidth=3, label="sortedness change")
        ax2.fill_between(x, monotonicity_std_down, monotonicity_std_up, color=color, alpha=0.1)
        ax2.tick_params(axis='y', labelcolor=color)
        # ax2.axhline(np.average(monotonicity_value_list), color='grey', linestyle='--', linewidth=0.5)
        # ax2.text(90, 52, 'bubble')
        # ax2.text(90, 46, 'selection')
    else:
        ax2.set_ylim(ymin=0, ymax=100)
        # find bubble
        b_monotonicity_value_list, b_monotonicity_std_up, b_monotonicity_std_down = get_average_monotonicity_array_for_cell_type(exps, 0)
        
        # find selection
        s_monotonicity_value_list, s_monotonicity_std_up, s_monotonicity_std_down = get_average_monotonicity_array_for_cell_type(exps, 1)

        # find insertion
        i_monotonicity_value_list, i_monotonicity_std_up, i_monotonicity_std_down = get_average_monotonicity_array_for_cell_type(exps, 2)
        
        if b_monotonicity_value_list:
            c_color = get_cell_color(0)
            ax2.plot(x, b_monotonicity_value_list, color=c_color, linewidth=1, label="bubble sortedness")
            ax2.fill_between(x, b_monotonicity_std_down, b_monotonicity_std_up, color=c_color, alpha=0.1)
            
        if s_monotonicity_value_list:
            c_color = get_cell_color(1)
            ax2.plot(x, s_monotonicity_value_list, color=c_color, linewidth=1, label="selection sortedness")
            ax2.fill_between(x, s_monotonicity_std_down, s_monotonicity_std_up, color=c_color, alpha=0.1)
        
        if i_monotonicity_value_list:
            c_color = get_cell_color(2)
            ax2.plot(x, i_monotonicity_value_list, color=c_color, linewidth=1, label="insertion sortedness")
            ax2.fill_between(x, i_monotonicity_std_down, i_monotonicity_std_up, color=c_color, alpha=0.1)
    
    print(f"max aggregation for {dir}: {max(aggregation_value_list)}, {aggregation_std_up[aggregation_value_list.index(max(aggregation_value_list))] - max(aggregation_value_list)}")
        
    ax2.legend(loc="upper right")
    
    # plt.savefig(f"/Users/tainingzhang/Desktop/research_images/claim_images/{file_name}_combined.png")
    # plt.show()

    # plt.figure()
    # plt.xlabel('sorting process pct')
    # plt.ylabel('aggregation value')
    # plt.title(title)
    # plt.plot(x, aggregation_value_list)
    # plt.show()


def get_first_step_aggregation_value(moves):
    return get_aggregation_value(moves[0])

def get_final_step_aggregation_value(moves):
    res = -1
    for m in moves:
        res = max(get_aggregation_value(m), res)
    return res

def get_max_aggregation_value(moves):
    r = 0
    for m in moves:
        r = max(r, get_aggregation_value_avg(m))
    return r

def get_experiment_data_set_v2(dir):
    first = []
    last = []
    for i in range(100):
        moves = np.load(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{dir}/exp_{i}.npy")
        first.append(get_aggregation_value_avg(moves[0]))
        last.append(get_max_aggregation_value(moves))
    return first, last


def get_experiment_data_set():
    first = []
    last = []
    for i in range(100):
        moves = np.load(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/cell_type_aggregation_random_dist_100_tests/exp_{i}.npy")
        first.append(get_first_step_aggregation_value(moves))
        last.append(get_final_step_aggregation_value(moves))
    return first, last

def get_ttest_value_for_aggregation_odds():
    expect, exp = get_experiment_data_set()
    print(np.mean(expect))
    print(np.mean(exp))
    print(get_ttest_value(exp, expect))

def get_ttest_value_for_aggregation_v2(dir):
    expect, exp = get_experiment_data_set_v2(dir)
    print(np.mean(expect))
    print(np.mean(exp))
    print(get_ttest_value(exp, expect))

def get_max_aggregation_map_at_exp(file_path):
    moves = np.load(file_path)
    max_aggregation_score_map = {}
    for move in moves:
        process_each_move(move, max_aggregation_score_map)
    return max_aggregation_score_map

def get_first_step_aggregation_map_at_exp(file_path):
    moves = np.load(file_path)
    max_aggregation_score_map = {}
    for move in moves:
        process_each_move(move, max_aggregation_score_map)
        break
    return max_aggregation_score_map

def get_x_pct_aggregation_map_at_exp(file_path, x):
    moves = np.load(file_path)
    max_aggregation_score_map = {}
    index = min(int(len(moves) * x), len(moves) - 1)
    process_each_move(moves[index], max_aggregation_score_map)
    return max_aggregation_score_map

def get_x_pct_avg_aggregation_map_over_all_exps(x):
    avg_aggregation_map = {}
    for i in range(100):
        max_aggregation_score_map = get_x_pct_aggregation_map_at_exp(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/cell_type_aggregation_random_dist_100_tests/exp_{i}.npy", x)
        for key in max_aggregation_score_map:
            if key not in avg_aggregation_map:
                avg_aggregation_map[key] = []
            avg_aggregation_map[key].append(max_aggregation_score_map[key])
    return avg_aggregation_map


def get_average_steps(dir):
    sorting_steps =  [len(np.load(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{dir}/exp_{i}.npy")) for i in range(100)]
    return np.average(sorting_steps)


def get_max_across_results(arr):
    res = []
    for i in range(len(arr[1])):
        max_value = -1
        for j in range(1, 11):
            max_value = max(arr[j][i], max_value)
        if max_value < 0:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>")
        res.append(max_value)
    return res


def get_observe_matrix():
    x_data = [y for y in range(1, 11)]
    # print(get_max_across_results(get_x_pct_avg_aggregation_map_over_all_exps(0.1)))
    pct_results = [get_max_across_results(get_x_pct_avg_aggregation_map_over_all_exps(0.1 * i)) for i in range(0, 11)]
    df = pd.DataFrame(pct_results)
    print(stats.chi2_contingency(df))
    
# plot_moves_file("cell_type_aggregation_random_dist_100_tests", "Bubble Selection Mix")
# plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_bubble_insertion", "Bubble Selection Mix")
# get_ttest_value_for_aggregation_v2("cell_type_aggregation_random_dist_100_tests")

# # # plot_moves_file("cell_type_aggregation_random_dist_100_tests_bubble_insertion", "Bubble Insertion Mix")
#plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_bubble_insertion", "Bubble Insertion Mix")
# get_ttest_value_for_aggregation_v2("cell_type_aggregation_random_dist_100_tests_bubble_insertion")

# # # plot_moves_file("cell_type_aggregation_random_dist_100_tests_selection_insertion", "Selection Insertion Mix")
# # plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_selection_insertion", "Selection Insertion Mix")
# get_ttest_value_for_aggregation_v2("cell_type_aggregation_random_dist_100_tests_selection_insertion")


# plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_bubble_selection_insertion", "Bubble Selection Insertion Mix")
# # get_ttest_value_for_aggregation_v2("cell_type_aggregation_random_dist_100_tests_bubble_selection_insertion")
# #fig = plt.figure(figsize = (20, 10))
def plot_cell_type_distribution():
    plot_max_aggregation_digits("cell_type_aggregation_random_dist_100_tests", "Bubble Selection Mix", [2, 2, 1])
    plot_max_aggregation_digits("cell_type_aggregation_random_dist_100_tests_bubble_insertion", "Bubble Insertion Mix", [2, 2, 2])
    plot_max_aggregation_digits("cell_type_aggregation_random_dist_100_tests_selection_insertion", "Selection Insertion Mix", [2, 2, 3])
    plot_max_aggregation_digits("cell_type_aggregation_random_dist_100_tests_bubble_selection_insertion", "Bubble Selection Insertion Mix", [2, 2, 4])
    plt.subplot_tool()
    plt.show()
# plot_cell_type_distribution()
    
# # # fig = plt.figure(figsize = (20, 10))
# plt.subplot(2, 2, 1)
def plot_aggregation_for_normal_aggregation():
    plt.figure(figsize = (20, 5))
    plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests", "Bubble Selection Mix", [1, 4], 1)
    plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_bubble_insertion", "Bubble Insertion Mix", [1, 4], 2)
    plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_selection_insertion", "Selection Insertion Mix", [1, 4], 3)
    plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_bubble_selection_insertion", "Bubble Selection Insertion Mix", [1, 4], 4, True)
    plt.subplot_tool()
    plt.show()
plot_aggregation_for_normal_aggregation()

def plot_move_based_on_other_move():
    plt.figure(figsize = (20, 10))
    plot_cell_monotonicity_change_by_other_cell_move("cell_type_aggregation_random_dist_100_tests", 'bubble', 'selection', [3, 2], 1)
    plot_cell_monotonicity_change_by_other_cell_move("cell_type_aggregation_random_dist_100_tests_bubble_insertion", 'bubble', 'insertion', [3, 2], 2)
    plot_cell_monotonicity_change_by_other_cell_move("cell_type_aggregation_random_dist_100_tests_bubble_selection_insertion", 'selection', 'insertion', [3, 2], 3)
# plot_move_based_on_other_move()
# plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_bubble_selection_disorder", "Bubble Selection Mix Disorder")
# plot_final_sorting_results("cell_type_aggregation_random_dist_100_tests_bubble_insertion", "Bubble Insertion Mix Disorder Final Result")
# plot_final_sorting_results("cell_type_aggregation_random_dist_100_tests_insertion_selection_disorder", "Selection Insertion Mix Disorder Final Result")
# plt.show()

def plot_dis_order_all():
    plt.figure(figsize = (20, 10))
    plot_dis_order("cell_type_aggregation_random_dist_100_tests_selection_bubble_disorder", "Selection Bubble Mix Disorder", "selection", "bubble", [1, 3, 1])
    plot_dis_order("cell_type_aggregation_random_dist_100_tests_bubble_insertion_random_disorder",  "Bubble Insertion Mix Random Disorder", "bubble", "insertion", [1, 3, 2])
    plot_dis_order("cell_type_aggregation_random_dist_100_tests_insertion_selection_disorder",  "Selection Insertion Mix Random Disorder", "insertion", "selection", [1, 3, 3])
    plt.subplot_tool()
    plt.show()
plot_dis_order_all()

def plot_all_aggregation_for_dup_aggregation():
    plt.figure(figsize = (20, 5))
    # plot_average_data_from_experiment("cell_type_aggregation_random_dist_1000_tests_bubble_selection_dup",  "Bubble Selection With Duplicates", [1, 1], 1)
    plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_bubble_insertion_dup",  "Bubble Insertion With Duplicates", [1, 3], 1, should_split=True)
    plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_bubble_selection_dup",  "Bubble Selection With Duplicates", [1, 3], 2, should_split=True)
    plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_selection_insertion_dup",  "Selection Insertion With Duplicates", [1, 3], 3, should_split=True)
    plt.subplot_tool()
    plt.show()
plot_all_aggregation_for_dup_aggregation()

# print(f"bubble inserstion: {get_average_steps('cell_type_aggregation_random_dist_100_tests_bubble_insertion')}")
# print(f"bubble selection: {get_average_steps('cell_type_aggregation_random_dist_100_tests')}")
# print(f"selection inserstion: {get_average_steps('cell_type_aggregation_random_dist_100_tests_selection_insertion')}")
# print(f"bubble: {get_average_steps('cell_type_aggregation_random_dist_100_tests_bubble_bubble')}")
# print(f"inserstion: {get_average_steps('cell_type_aggregation_random_dist_100_tests_insertion_insertion')}")
# print(f"selection: {get_average_steps('cell_type_aggregation_random_dist_100_tests_selection_selection')}")
# print(get_average_steps("cell_type_aggregation_random_dist_100_tests"))
# print(get_average_steps("cell_type_aggregation_random_dist_100_tests_selection_insertion"))
# print(get_average_steps("cell_type_aggregation_random_dist_100_tests_bubble_bubble"))
# print(get_average_steps("cell_type_aggregation_random_dist_100_tests_insertion_insertion"))
# print(get_average_steps("cell_type_aggregation_random_dist_100_tests_selection_selection"))


# # plt.subplot(2, 3, 1)
# plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests", "Bubble Selection Mix", 1)
# # plt.subplot(2, 3, 2)
# plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_bubble_insertion", "Bubble Insertion Mix", 2)
# # plt.subplot(2, 3, 3)
# plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_selection_insertion", "Selection Insertion Mix", 3)
# # plt.subplot(2, 3, 4)
# plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_bubble_bubble", "Bubble Bubble Mix", 4)
# # plt.subplot(2, 3, 5)
# plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_insertion_insertion", "Insertion Insertion Mix", 5)
# # plt.subplot(2, 3, 6)
# plot_average_data_from_experiment("cell_type_aggregation_random_dist_100_tests_selection_selection", "Selection Selection Mix", 6)
# plt.show()
# get_ttest_value_for_aggregation_v2("cell_type_aggregation_random_dist_100_tests_bubble_bubble")


# results, first_step_results = get_avg_aggregation_map_over_all_exps()

# print(results)
# print(first_step_results)

# plt.figure()
# x_data = [y for y in range(1, 11)]
# expect_y_data = [np.average(first_step_results[x]) for x in x_data]
# expect_y_upper_data = [np.average(first_step_results[x]) + np.std(first_step_results[x]) for x in x_data]
# expect_y_lower_data = [np.average(first_step_results[x]) - np.std(first_step_results[x]) for x in x_data]
# plt.fill_between(x_data, expect_y_lower_data, expect_y_upper_data, color='r', alpha=0.1)
# print(">>>>>>>>>>>>>>>>>>>")
# print(expect_y_data)
# plt.plot(x_data, expect_y_data, color='r', linestyle='-', label='expect value')
# y_data = [np.average(results[x]) for x in x_data]
# y_upper_data = [np.average(results[x]) + np.std(results[x]) for x in x_data]
# y_lower_data = [np.average(results[x]) - np.std(results[x]) for x in x_data]

# ttest_data = [get_ttest_value(results[x], first_step_results[x]) for x in x_data]
# print(y_data)
# print(ttest_data)
# plt.plot(x_data, y_data, color='b', linestyle='-', label='experiment value')
# plt.fill_between(x_data, y_lower_data, y_upper_data, color='b', alpha=0.1)
# plt.legend(loc='best')
# plt.show()

# # bins = [0 for _ in range(20)]
# # for s in samples:
# #     b_index = int(s / 5)
# #     bins[b_index] += 1
# # print(bins)

# counts = {} 

# for s in samples:
#     if s in counts:
#         counts[s] += 1
#     else:
#         counts[s] = 1

# # sns.distplot(samples, hist=True,
# #              bins=int(12), color = 'darkblue', 
# #              hist_kws={'edgecolor':'black'})
# # plt.show()


# # xdata = [ -10.0, -9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
# # ydata = [1.2, 4.2, 6.7, 8.3, 10.6, 11.7, 13.5, 14.5, 15.7, 16.1, 16.6, 16.0, 15.4, 14.4, 14.2, 12.7, 10.3, 8.6, 6.1, 3.9, 2.1]
  
# # Recast xdata and ydata into numpy arrays so we can use their handy features
# # xdata = np.asarray([k for k in counts.keys()])
# # xdata.sort()
# # ydata = 50 * stats.norm.pdf(xdata, 7, 1)
# # plt.plot(xdata, ydata, '-')
  
# # plt.legend()
# # plt.show()
# mu = np.average(samples)
# sigma = np.std(samples)
# num_bins = 10
# m = {}
# for s in samples:
#     if s in m:
#         m[s] += 1
#     else:
#         m[s] = 1 
# bins = [k for k in m.keys()]
# bins.sort()
# print(bins)
# for b in bins:
#     print(m[int(b)])
# n, bins, patches = plt.hist(samples, bins=bins, 
#                             color ='green',
#                             alpha = 1)

   
# expected = 1000* (((1 / (np.sqrt(2 * np.pi) * sigma)) *
#      np.exp(-0.5 * (1 / sigma * (bins - mu))**2)))
# for e in expected:
#     print(f'{e: .2f}')

# fit_bins = [] 
# left_bound = min(samples)
# while left_bound <= max(samples):
#     fit_bins.append(left_bound)
#     left_bound += 0.1
# y =  1000 * (((1 / (np.sqrt(2 * np.pi) * sigma)) *
#      np.exp(-0.5 * (1 / sigma * (fit_bins - mu))**2)))
  
# plt.plot(fit_bins, y, '--', color ='black')
  
# plt.xlabel('X-Axis')
# plt.ylabel('Y-Axis')
  
  
# plt.show()


# def get_max_consecutive_num(arr, t):
#     res = 0
#     count = 0
#     for n in arr:
#         if n == t:
#             count+=1
#         else:
#             count = 0 
#         res = max(res, count)
#     res = max(res, count)
#     return res  


# def get_avg_cluster_size(arr, t):
#     res = 0
#     count = 0
#     for n in arr:
#         if n == t:
#             count = 1
#         else:
#             res += count 
#             count = 0
#     res += count 
#     return 50 / res

# def get_cluster_size_list(arr, t):
#     res = []
#     cluster_size = 0
#     for n in arr:
#         if n == t:
#             cluster_size += 1
#         else:
#             if cluster_size:
#                 res.append(cluster_size)
#             cluster_size = 0
#     if cluster_size:
#         res.append(cluster_size)
#     return res



# consecutive_one_clusters = [get_cluster_size_list(arr, 1) for arr in moves]
# consecutive_zero_clusters = [get_cluster_size_list(arr, 0) for arr in moves]


# consecutive_ones_avg_size = [np.average(arr) for arr in consecutive_one_clusters]
# consecutive_zeros_avg_size = [np.average(arr) for arr in consecutive_zero_clusters]

# ones_max_cluster_size = [max(step) for step in consecutive_one_clusters]
# zeroes_max_cluster_size = [max(step) for step in consecutive_zero_clusters]

# ones_cluster_size_std = [np.std(step) for step in consecutive_one_clusters]
# zeroes_cluster_size_std = [np.std(step) for step in consecutive_zero_clusters]

# plt.figure()
# plt.xlabel('time')
# plt.ylabel('max cluster size')

# x = [n for n in range(len(consecutive_one_clusters))]

# plt.yticks(np.arange(min(consecutive_ones_avg_size), max(ones_max_cluster_size)+1, 1))

# plt.plot(x, consecutive_ones_avg_size, color='r', label="bubble cell cluster size avg",)
# plt.plot(x, consecutive_zeros_avg_size, color='b', label='selection cell cluster size avg')

# plt.plot(x, ones_max_cluster_size, color='g', label="bubble cell cluster max size",)
# plt.plot(x, zeroes_max_cluster_size, color='y', label='selection cell cluster max size')

# plt.plot(x, ones_cluster_size_std, color='c', label="bubble cell cluster size std",)
# plt.plot(x, zeroes_cluster_size_std, color='m', label='selection cell cluster size std')

# plt.legend(loc='best')

# plt.show()

