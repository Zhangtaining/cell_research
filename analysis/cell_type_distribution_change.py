import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.patheffects import PathPatchEffect, SimpleLineShadow, Normal, Stroke
from scipy import stats
import seaborn as sns
from scipy.optimize import curve_fit

# moves = np.load('/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/cell_type_with_group_id_evenly_dist.npy')
def get_cell_type_in_each_group(arr):
    group_map = {}
    for [key, value] in arr:
        if key not in group_map:
            group_map[key] = []
        group_steps = group_map[key]
        group_steps.append(value)
    return group_map

def update_cell_type_map(overall_map, c_map):
    for key in c_map:
        if key in overall_map:
            if not same_step(overall_map[key][-1], c_map[key]):
                overall_map[key].append(c_map[key])
        else:
            overall_map[key] = [c_map[key]]

def same_step(arr1, arr2):
    if len(arr1) != len(arr2):
        return False 
    
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False 
    
    return True

def get_homogenity_in_each_group(move):
    group_id = -1
    b_count = 0
    s_count = 0
    res = []
    for [g_id, c_type] in move:
        if g_id != group_id:
            if group_id != -1:
                res.append(abs(b_count - s_count))
            group_id = g_id
            b_count = 0
            s_count = 0
        if c_type == 1:
            b_count+=1
        if c_type == 0:
            s_count += 1
    res.append(abs(b_count - s_count))
    return res


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


def get_max_homogenity_at_exp(file_path):
    moves = np.load(file_path)
    homogenity_at_each_move = trim_the_list([get_homogenity_in_each_group(move) for move in moves])
    return max([max(homogenity) for homogenity in homogenity_at_each_move])


def get_all_exps_max_homogenity():
    return [get_max_homogenity_at_exp(f"/Users/tainingzhang/Workspace/research/sorting_with_noise/cell_sorting/csv/cell_type_with_group_id_random_dist_1000_tests/exp_{i}.npy") for i in range(1000)]


def calculate_t_value(arr):
    mean = np.average(arr)
    print(mean)
    std = np.std(arr)
    print(std)
    u = 0
    sample_size = 50
    return (mean - 1) / (std / math.sqrt(sample_size))

def calculate_p_value(t):
    return scipy.stats.t.sf(abs(t), df=22)*2


samples = get_all_exps_max_homogenity()
# bins = [0 for _ in range(20)]
# for s in samples:
#     b_index = int(s / 5)
#     bins[b_index] += 1
# print(bins)

counts = {} 

for s in samples:
    if s in counts:
        counts[s] += 1
    else:
        counts[s] = 1

# sns.distplot(samples, hist=True,
#              bins=int(12), color = 'darkblue', 
#              hist_kws={'edgecolor':'black'})
# plt.show()


# xdata = [ -10.0, -9.0, -8.0, -7.0, -6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
# ydata = [1.2, 4.2, 6.7, 8.3, 10.6, 11.7, 13.5, 14.5, 15.7, 16.1, 16.6, 16.0, 15.4, 14.4, 14.2, 12.7, 10.3, 8.6, 6.1, 3.9, 2.1]
  
# Recast xdata and ydata into numpy arrays so we can use their handy features
# xdata = np.asarray([k for k in counts.keys()])
# xdata.sort()
# ydata = 50 * stats.norm.pdf(xdata, 7, 1)
# plt.plot(xdata, ydata, '-')
  
# plt.legend()
# plt.show()
mu = np.average(samples)
sigma = np.std(samples)
num_bins = 10
m = {}
for s in samples:
    if s in m:
        m[s] += 1
    else:
        m[s] = 1 
bins = [k for k in m.keys()]
bins.sort()
print(bins)
for b in bins:
    print(m[int(b)])
n, bins, patches = plt.hist(samples, bins=bins, 
                            color ='green',
                            alpha = 1)

   
expected = 1000* (((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (bins - mu))**2)))
for e in expected:
    print(f'{e: .2f}')

fit_bins = [] 
left_bound = min(samples)
while left_bound <= max(samples):
    fit_bins.append(left_bound)
    left_bound += 0.1
y =  1000 * (((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (fit_bins - mu))**2)))
  
plt.plot(fit_bins, y, '--', color ='black')
  
plt.xlabel('X-Axis')
plt.ylabel('Y-Axis')
  
  
plt.show()


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

