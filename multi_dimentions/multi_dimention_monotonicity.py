import matplotlib.pyplot as plt
import numpy as np
import random
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
from statsmodels.stats.weightstats import ztest as ztest
# import statistics as st

def get_current_monotonicity(arr):
        monotonicity_value = 0
        prev = arr[0]
        for i in range(1, len(arr)):
            if arr[i] >= prev:
                monotonicity_value += 1
            prev = arr[i]
        return monotonicity_value


def random_pick_color():
    r = random.random()
    b = random.random()
    g = random.random()
    return (r, g, b)

def get_sorting_steps_arr(file):
    loaded_data = np.load(file, allow_pickle=True,)
    return [len(moves) for moves in loaded_data]

def get_sorting_steps(file):
    return np.load(file, allow_pickle=True,)

def cell_original_efficiency_compare_include_read():
    cell_bubble_steps = get_sorting_steps('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_with_0frozen_total_steps_100exps.npy') 
    original_bubble_steps = get_sorting_steps('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_bubble_sort_sorting_with_0frozen_total_steps_100exps.npy')
    
    cell_insertion_steps = get_sorting_steps('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/insertion_sort_sorting_with_0frozen_total_steps_100exps.npy') 
    original_insertion_steps = get_sorting_steps('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_insertion_sort_sorting_with_0frozen_total_steps_100exps.npy')
    
    cell_selection_steps = get_sorting_steps('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_sorting_with_0frozen_total_steps_100exps.npy') 
    original_selection_steps = get_sorting_steps('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_selection_sort_sorting_with_0frozen_total_steps_100exps.npy')
    ztest_bubble = ztest(cell_bubble_steps, original_bubble_steps)
    ztest_insertion =  ztest(cell_insertion_steps, original_insertion_steps)
    ztest_selection = ztest(cell_selection_steps, original_selection_steps)
    print("bubble")
    print(ztest_bubble)
    print("insertion")
    print(ztest_insertion)
    print("selection")
    print(ztest_selection)
    barWidth = 0.25
    # fig = plt.subplots(figsize =(12, 8))
    
    # set height of bar
    original = [np.average(original_bubble_steps), np.average(original_insertion_steps), np.average(original_selection_steps)]
    cell = [np.average(cell_bubble_steps), np.average(cell_insertion_steps), np.average(cell_selection_steps)]
    
    original_std = [np.std(original_bubble_steps), np.std(original_insertion_steps), np.std(original_selection_steps)]
    cell_std = [np.std(cell_bubble_steps), np.std(cell_insertion_steps), np.std(cell_selection_steps)]
    print(original_std)
    print(cell_std)
    # Set position of bar on X axis
    br1 = np.arange(len(original))
    br2 = [x + barWidth for x in br1]
    
    # Make the plot
    plt.bar(br1, original, color ='r', width = barWidth,
            edgecolor ='grey', label ='Traditional', yerr=original_std)
    plt.bar(br2, cell, color ='g', width = barWidth,
            edgecolor ='grey', label ='Cell', yerr=cell_std)
    
    # Adding Xticks
    plt.ylabel('Swapping & Reading Steps', fontweight ='bold', fontsize = 8)
    plt.xticks([r + barWidth / 2 for r in range(len(original))],
            ['bubble', 'insertion', 'selection'], fontsize = 10)
    
    
    plt.title(f'Cell and Traditional Efficiency Comparison')
    
    plt.legend()
    # plt.savefig(f"/Users/tainingzhang/Desktop/research_images/claim_images/cell_traditional_efficiency_comparison.png")
    # plt.show()
def get_sorting_steps_for_aggregation(file_path):
    steps = []
    for i in range(100):
        moves = np.load(f"{file_path}/exp_{i}.npy")
        steps.append(len(moves))
        
    return steps

def cell_efficiency_mix_compare():
    cell_bubble_steps = get_sorting_steps_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_with_0frozen_cannot_move_steps_100exps.npy')     
    cell_insertion_steps = get_sorting_steps_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/insertion_sort_sorting_with_0frozen_cannot_move_steps_100exps.npy')     
    cell_selection_steps = get_sorting_steps_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_sorting_with_0frozen_cannot_move_steps_100exps.npy') 
    cell_bubble_selection_steps = get_sorting_steps_for_aggregation("/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/cell_type_aggregation_random_dist_100_tests")
    cell_bubble_insertion_steps = get_sorting_steps_for_aggregation("/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/cell_type_aggregation_random_dist_100_tests_bubble_insertion")
    cell_insertion_selection_steps = get_sorting_steps_for_aggregation("/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/cell_type_aggregation_random_dist_100_tests_selection_insertion")
    cell = [np.average(cell_bubble_steps), np.average(cell_insertion_steps), np.average(cell_selection_steps), np.average(cell_bubble_selection_steps), np.average(cell_bubble_insertion_steps), np.average(cell_insertion_selection_steps)]
    cell_std = [np.std(cell_bubble_steps), np.std(cell_insertion_steps), np.std(cell_selection_steps), np.std(cell_bubble_selection_steps), np.std(cell_bubble_insertion_steps), np.std(cell_insertion_selection_steps)]
    barWidth = 0.25
    
    br1 = np.arange(len(cell))
    
    # Make the plot
    plt.bar(br1, cell, color ='g', width = barWidth,
            edgecolor ='grey', yerr=cell_std)

    
    # Adding Xticks
    plt.ylabel('Swapping Steps', fontweight ='bold', fontsize = 25)
    plt.xticks([r for r in range(len(cell))],
            ['bubble', 'insertion', 'selection', 'bubble & selection mix', 'bubble & insertion mix', 'insertion & selection mix'], fontsize = 25)
    
    plt.title(f'Single Cell and Mixed Cell Efficiency Comparison', fontsize=25)
    
    plt.show()
    
    
    

def cell_original_efficiency_compare():
    cell_bubble_steps = get_sorting_steps_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_with_0frozen_cannot_move_steps_100exps.npy') 
    original_bubble_steps = get_sorting_steps_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_bubble_sort_with_0frozen_cannot_move_sorting_steps_100exps.npy')
    
    cell_insertion_steps = get_sorting_steps_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/insertion_sort_sorting_with_0frozen_cannot_move_steps_100exps.npy') 
    original_insertion_steps = get_sorting_steps_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_insertion_sort_with_0frozen_cannot_move_sorting_steps_100exps.npy')
    
    cell_selection_steps = get_sorting_steps_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_sorting_with_0frozen_cannot_move_steps_100exps.npy') 
    original_selection_steps = get_sorting_steps_arr('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_selection_sort_with_0frozen_cannot_move_sorting_steps_100exps.npy')
    
    ztest_bubble = ztest(cell_bubble_steps, original_bubble_steps)
    ztest_insertion =  ztest(cell_insertion_steps, original_insertion_steps)
    ztest_selection = ztest(cell_selection_steps, original_selection_steps)
    print("bubble")
    print(ztest_bubble)
    print("insertion")
    print(ztest_insertion)
    print("selection")
    print(ztest_selection)
    
    barWidth = 0.25
    # fig = plt.subplots(figsize =(12, 8))
    
    # set height of bar
    original = [np.average(original_bubble_steps), np.average(original_insertion_steps), np.average(original_selection_steps)]
    cell = [np.average(cell_bubble_steps), np.average(cell_insertion_steps), np.average(cell_selection_steps)]
    
    original_std = [np.std(original_bubble_steps), np.std(original_insertion_steps), np.std(original_selection_steps)]
    cell_std = [np.std(original_bubble_steps), np.std(original_insertion_steps), np.std(original_selection_steps)]
    
    print(cell_std)
    
    # Set position of bar on X axis
    br1 = np.arange(len(original))
    br2 = [x + barWidth for x in br1]
    
    # Make the plot
    plt.bar(br1, original, color ='r', width = barWidth,
            edgecolor ='grey', label ='Traditional', yerr=original_std)
    plt.bar(br2, cell, color ='g', width = barWidth,
            edgecolor ='grey', label ='Cell', yerr=cell_std)
    
    # Adding Xticks
    plt.ylabel('Swapping Steps', fontweight ='bold', fontsize = 8)
    plt.xticks([r + barWidth / 2 for r in range(len(original))],
            ['bubble', 'insertion', 'selection'], fontsize = 10)
    
    plt.title(f'Cell and Traditional Efficiency Comparison')
    
    plt.legend()
    # plt.savefig(f"/Users/tainingzhang/Desktop/research_images/claim_images/cell_traditional_efficiency_comparison.png")
    # plt.show()
    

def plot_data_with_zoom_in():

    f, ax = plt.subplots(1, figsize = (8, 5))
    plt.xlabel('swap steps',  fontsize = 13)
    plt.ylabel('sortedness',  fontsize = 15)
    plt.title("Cell Sorting Sortedness Change", fontsize = 15)
    moves = np.load('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_with_0frozen_cannot_move_steps_100exps.npy', allow_pickle=True)[0]
    monotonicities = [get_current_monotonicity(arr) for  arr in moves]
    x = [n for n in range(1, len(monotonicities) +1)]
    ax.plot(x, monotonicities)
    axins = zoomed_inset_axes(ax, zoom=2, loc='upper right', borderpad=1.0)
    axins.plot(x, monotonicities, c='b')
    axins.yaxis.set_visible(False)
    axins.xaxis.set_visible(False)
    for s in ['top', 'bottom', 'left', 'right']:
        axins.spines[s].set(color='grey', lw=1, linestyle='solid')
    axins.set(xlim=[500, 680], ylim=[62, 80])
    mark_inset(ax, axins, loc1=2, loc2=4, fc='none', ec='gray')

    ax.legend(loc='upper left', frameon=False)
    ax.set(xlim=[0, len(monotonicities)])
    plt.show()


def plot_raw_data(file, color=None, l=None, algo="", frozen_cell=0):
    plt.xlabel('swap steps')
    # plt.ylabel('monotonicity')
    algo_name = algo.replace('_', ' ')
    # plt.title(f'{algo_name} with {frozen_cell} frozen cells')
    loaded_data = np.load(file, allow_pickle=True,)
    for moves in loaded_data:
        monotonicities = [get_current_monotonicity(arr) for  arr in moves]
        x = [n for n in range(1, len(monotonicities) +1)]
        plt.plot(x, monotonicities, c=random_pick_color() if color is None else color, label=l)
        #break
    # plt.savefig(f"/Users/tainingzhang/Desktop/research_images/claim_images/{algo}_{frozen_cell}_monotonicity_error_change.png")
    # plt.show()
    

def find_sortness_decreasing():
    cell_file = f'/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_with_0frozen_cannot_move_steps_100exps.npy'
    loaded_data = np.load(cell_file, allow_pickle=True,)
    random_exp = loaded_data[random.randint(0, len(loaded_data))]
    for i in range(1, len(random_exp)):
        prev_step = random_exp[i - 1]
        step = random_exp[i]
        prev_monotonicity = get_current_monotonicity(prev_step)
        current_monotonicity = get_current_monotonicity(step)
        if current_monotonicity < prev_monotonicity:
            print(prev_step)
            print(step)
            return 
    
    
    
def plot_tranditional_cell_together(frozen_cell, cell_type):
    # cell_types = ['bubble_sort', 'insertion_sort', 'selection_sort']
    fig = plt.figure(figsize = (12, 4))
    algo_name = cell_type.replace('_', ' ')
    fig.supylabel(algo_name, weight = 'bold', fontsize = 14)
    # for i in range(3):
    #     cell_type = cell_types[i]
    traditional_file = f'/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_{cell_type}_with_{frozen_cell}frozen_cannot_move_sorting_steps_100exps.npy'
    cell_file = f'/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{cell_type}_sorting_with_{frozen_cell}frozen_cannot_move_steps_100exps.npy'
    plt.subplot(1, 2, 1)
    plot_raw_data_for_original_algo(traditional_file, algo=cell_type)
    plt.title("Traditional", weight = 'bold', fontsize = 12)
    plt.subplot(1, 2, 2)
    plot_raw_data(cell_file, algo=cell_type)
    plt.title("Cell View", weight = 'bold', fontsize = 12)
    
    plt.show()

def plot_raw_data_for_original_algo(file, color=None, l=None, algo="", frozen_cell=0):
    plt.xlabel('swap steps')
    plt.ylabel('monotonicity error')
    
    plt.ylabel("Sortedness", fontsize = 12)
    loaded_data = np.load(file, allow_pickle=True,)
    for moves in loaded_data:
        monotonicities = moves
        x = [n for n in range(1, len(monotonicities) +1)]
        plt.plot(x, monotonicities, c=random_pick_color() if color is None else color, label=l)
        #break
    
# for algorithm in ['bubble_sort', 'insertion_sort', 'selection_sort']:
#     for frozen_cell_number in [0, 1, 2, 3]:
#         plt.subplot(2, 2, frozen_cell_number + 1)
#         plot_raw_data(f'/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{algorithm}_sorting_with_{frozen_cell_number}frozen_steps_100exps.npy', algo=algorithm, frozen_cell=frozen_cell_number)
#     plt.savefig(f"/Users/tainingzhang/Desktop/research_images/claim_images/{algorithm}_monotonicity_error_change_all.png")
#     plt.show()

# for algorithm in ['original_bubble_sort', 'original_insertion_sort', 'original_selection_sort']:
#     for frozen_cell_number in [0, 1, 2, 3]:
#         plt.subplot(2, 2, frozen_cell_number + 1)
#         plot_raw_data_for_original_algo(f'/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{algorithm}_with_{frozen_cell_number}frozen_cannot_move_sorting_steps_100exps.npy', algo=algorithm, frozen_cell=frozen_cell_number)
#     plt.savefig(f"/Users/tainingzhang/Desktop/research_images/claim_images/{algorithm}_monotonicity_error_change_all.png")
#     plt.show()
# def plot_together_reading_swapping():
#     plt.subplot(2, 1, 1)
#     cell_original_efficiency_compare()
#     plt.subplot(2, 1, 2)
#     cell_original_efficiency_compare_include_read()
#     plt.subplot_tool()
#     plt.show()
    
# plot_together_reading_swapping()

# cell_original_efficiency_compare_include_read()
# plot_tranditional_cell_together(0, 'bubble_sort')
# plot_tranditional_cell_together(0, 'insertion_sort')
# plot_tranditional_cell_together(0, 'selection_sort')

cell_efficiency_mix_compare()

# cell_original_efficiency_compare()

# plot_data_with_zoom_in()

# find_sortness_decreasing()

# plot_raw_data(f'/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_sorting_with_5frozen_steps_100exps.npy')
# for frozen_cell_number in [0, 1, 2, 3]:
#     for algorithm in ['bubble_sort', 'insertion_sort', 'selection_sort']:
#         c = 'r'
#         if algorithm == 'bubble_sort':
#             c = 'r'
#         if algorithm == 'insertion_sort':
#             c = 'g'
#         if algorithm == 'selection_sort':
#             c = 'b'
#         plot_raw_data(f'/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/{algorithm}_sorting_with_{frozen_cell_number}frozen_cannot_move_steps_100exps.npy', color=c, l=algorithm)
#     plt.legend(loc='best')
#     plt.show()


# plot_raw_data('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_sorting_with_2frozen_steps_100exps.npy', color='g')
# plot_raw_data('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/selection_sort_sorting_with_3frozen_steps_100exps.npy', color='b')

# plot_raw_data_for_original_algo('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/original_bubble_sort_with_forzen_sorting_steps_100exps.npy')

# def check_wandering_range(arr):
#     current_min = arr[0]
#     peak = -1
#     res = 0
#     for i in range(1, len(arr)):
#         p = arr[i - 1]
#         c = arr[i]
#         if c - p < 0:
#             if peak != -1:
#                 res += peak - current_min
#             peak = -1
#             current_min = c 
        
#         if c - p > 0:
#             peak = c

#     if peak != -1:
#         res += peak - current_min
#     return res

# def check_minimum_breaking_times(arr):
#     prev = 100000000
#     res = 0
#     for n in arr:
#         if n > prev:
#             res += 1 
#         prev = n 
#     return res

# def ability_to_break_local_minimum(file, pct):
#     loaded_data = np.load(file, allow_pickle=True,)
#     monotonicities_for_each_exp = []
#     for moves in loaded_data:
#         #monotonicities_for_each_exp.append([get_current_monotonicity(arr) for  arr in moves])
#         monotonicities_for_each_exp.append([check_wandering_range(arr) for arr in moves])
#     minimum_breaking_list = [check_minimum_breaking_times(arr) for arr in monotonicities_for_each_exp]


#     print(f"Averge for each combination Bubble {pct}% >>>>>>>>>>>>>>>>>")
#     print(f"Avg of minimum breaking times: {np.average(minimum_breaking_list)}")
#     print(f"Median of minimum breaking times: {st.median(minimum_breaking_list)}")
#     print(f"Max of minimum breaking times: {max(minimum_breaking_list)}")
#     print(f"Std of minimum breaking times: {np.std(minimum_breaking_list)}")



# # plot_raw_data('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_p0_steps_for_50_exp.npy')
# # plot_raw_data('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_p25_steps_for_50_exp.npy')
# # plot_raw_data('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_p50_steps_for_50_exp.npy')
# # plot_raw_data('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_p75_steps_for_50_exp.npy')

# ability_to_break_local_minimum('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_p0_steps_for_50_exp.npy', 0)
# ability_to_break_local_minimum('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_p25_steps_for_50_exp.npy', 25)
# ability_to_break_local_minimum('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_p50_steps_for_50_exp.npy', 50)
# ability_to_break_local_minimum('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_p75_steps_for_50_exp.npy', 75)
# ability_to_break_local_minimum('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_steps_for_50_exps.txt.npy', 100)






