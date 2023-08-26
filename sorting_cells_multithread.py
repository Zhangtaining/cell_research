import sys
import threading
import time
from modules.multithread.MultiThreadCell import MultiThreadCell

#VALUE_LIST = [28, 34, 6, 20, 7, 89, 34, 18, 29, 51]
VALUE_LIST = range(50,0,-1)

threadLock = threading.Lock()

def create_cells_based_on_value_list(value_list):
    if len(value_list) == 0:
        return []
    cells = []
    start_cell = MultiThreadCell(0, 0, threadLock, None)
    current_cell = start_cell
    for i in range(0, len(value_list)):
        cell = MultiThreadCell(i + 1, VALUE_LIST[i], threadLock, start_cell)
        cells.append(cell)
        cell.left_neighbor = current_cell
        current_cell.right_neighbor = cell 
        current_cell = cell

    return cells, start_cell 

def get_values_as_arr(start_ptr):
    p = start_ptr.right_neighbor
    values = []
    while p:
        values.append(p.value)
        p = p.right_neighbor
    return values

def print_current_list(start_ptr):
    threadLock.acquire()
    values = get_values_as_arr(start_ptr)
    print(values)
    threadLock.release()


def sort_cells(cells, start_ptr):
    for cell in cells:
        cell.start()


def get_current_monotonicity(arr, index):
        monotonicity_value = 0
        prev = arr[0][index]
        for i in range(1, len(arr)):
            if arr[i][index] < prev:
                monotonicity_value += 1
            prev = arr[i][index]
        return monotonicity_value

def main(argv):
    cells, start_ptr = create_cells_based_on_value_list(VALUE_LIST)
    sort_cells(cells, start_ptr)
    while True:
        print_current_list(start_ptr)
        time.sleep(0.0001)
        

if __name__ == "__main__":
    main(sys.argv[1:])