import matplotlib.pyplot as plt
import numpy as np
import random
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
# import statistics as st

def get_current_monotonicity(arr):
        monotonicity_value = 0
        prev = arr[0]
        for i in range(1, len(arr)):
            if arr[i] < prev:
                monotonicity_value += 1
            prev = arr[i]
        return monotonicity_value


f, ax = plt.subplots(1, figsize = (8, 4))
plt.xlabel('time')
plt.ylabel('monocity')
moves = np.load('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/bubble_sort_steps_for_1_exp.npy')[0]
monotonicities = [get_current_monotonicity(arr) for  arr in moves]
x = [n for n in range(1, len(monotonicities) +1)]
ax.plot(x, monotonicities)
axins = zoomed_inset_axes(ax, zoom=3, loc='upper right', borderpad=1.0)
axins.plot(x, monotonicities, c='b')
axins.yaxis.set_visible(False)
axins.xaxis.set_visible(False)
for s in ['top', 'bottom', 'left', 'right']:
    axins.spines[s].set(color='grey', lw=1, linestyle='solid')
axins.set(xlim=[300, 500], ylim=[20, 30])
mark_inset(ax, axins, loc1=2, loc2=4, fc='none', ec='gray')

ax.legend(loc='upper left', frameon=False)
ax.set(xlim=[0, len(monotonicities)], title='Zoomed inset axis')
plt.show()

# def random_pick_color():
#     r = random.random()
#     b = random.random()
#     g = random.random()
#     return (r, g, b)

# def plot_raw_data(file):
#     loaded_data = np.load(file, allow_pickle=True,)
#     for moves in loaded_data:
#         monotonicities = [get_current_monotonicity(arr) for  arr in moves]
#         x = [n for n in range(1, len(monotonicities) +1)]
#         plt.plot(x, monotonicities, c=random_pick_color())

#     plt.show()

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






