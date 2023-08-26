
def get_monotonicity(arr):
    monotonicity_value = 1
    prev = arr[0]
    for i in range(1, len(arr)):
        if arr[i] >= prev:
            monotonicity_value += 1
        prev = arr[i]
    return (monotonicity_value / len(arr)) * 100

def get_spearman_distance(arr):
    res = 0
    for i in range(len(arr)):
        res += abs(arr[i] - i)
    return res
