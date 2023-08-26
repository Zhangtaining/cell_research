import sys, getopt
from tkinter import * 
import threading
import time
from modules.multithread.SelectionSortCell import SelectionSortCell
from modules.multithread.BubbleSortCell import BubbleSortCell
from modules.multithread.InsertionSortCell import InsertionSortCell
from modules.multithread.MergeSortCell import MergeSortCell
from modules.multithread.CellGroup import CellGroup, GroupStatus
from modules.multithread.MultiThreadCell import CellStatus
from visualization.CellImage import CellImage
from visualization.CellGroupImage import CellGroupImage
from modules.multithread.StatusProbe import StatusProbe
import numpy as np
import random


VALUE_LIST = [28, 34, 6, 20, 7, 89, 34, 18, 29, 51]
#VALUE_LIST = range(20,0,-1)

def get_cell_type_list(total_cells, should_shuffle, bubble_pct):
    bubble_cell_num = int(total_cells * bubble_pct)
    selection_cell_num = total_cells - bubble_cell_num
    b_list = [1 for _ in range(bubble_cell_num)]
    s_list = [0 for _ in range(selection_cell_num)]
    combined_list = []
    for i in range(max(bubble_cell_num, selection_cell_num)):
        if i < bubble_cell_num:
            combined_list.append(b_list[i])
        if i < selection_cell_num:
            combined_list.append(s_list[i])
    if should_shuffle:
        random.shuffle(combined_list)
    
    return combined_list

def get_cell_type_list_v2(total_cells_per_type, generate_bubble, generate_selection, generate_insertion):
    combined_list = []
    if generate_bubble:
        b_list = [0 for _ in range(total_cells_per_type)]
        combined_list.extend(b_list)

    if generate_insertion:
        b_list = [1 for _ in range(total_cells_per_type)]
        combined_list.extend(b_list)
        
    if generate_selection:
        b_list = [2 for _ in range(total_cells_per_type)]
        combined_list.extend(b_list)

    random.shuffle(combined_list)

    return combined_list

def create_cell_groups_based_on_value_list(value_list, threadLock, status_probe, total_cells_per_type, generate_bubble, generate_selection, generate_insertion):
    if len(value_list) == 0:
        return []
    cells = []
    cell_groups = []
    cell_type_list = get_cell_type_list_v2(total_cells_per_type, generate_bubble, generate_selection, generate_insertion)
    if len(cell_type_list) != len(value_list):
        raise BaseException("unmatch cell number")
    left_boundary = (0, 1)
    right_boundary = (len(value_list) - 1, 1)
    for i in range(0, len(value_list)):
        cell = None
        cell_type_number = cell_type_list[i]
        if cell_type_number == 0:
            cell = BubbleSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, left_boundary, right_boundary, status_probe, disable_visualization=True)
        if cell_type_number == 1:
            cell = InsertionSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, left_boundary, right_boundary, status_probe, disable_visualization=True)
        if cell_type_number == 2:
            cell = SelectionSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, left_boundary, right_boundary, status_probe, disable_visualization=True)
        period = random.randint(100000, 200000000)
        start_count_down = random.randint(100000, 200000000)
        cell_group = CellGroup([cell], cells, i, (i, 1), (i, 1), GroupStatus.SLEEP, threadLock, start_count_down, period)
        # cell.group = cell_group

        if cell:
            cells.append(cell)
    # cells[random.randint(0, len(cells) - 1 )].set_cell_to_freeze()

    period = 1000000000
    start_count_down = 1000000000
    cell_group = CellGroup(cells, cells, 0, left_boundary, right_boundary, GroupStatus.ACTIVE, threadLock, start_count_down, period)
    for cell in cells:
        cell.group = cell_group 

    return cells, [cell_group]

def check_cell_status(cells):
    prev_cell = cells[0]
    for c in cells:
        if c.value < prev_cell.value:
            return True
        prev_cell = c
    
    for c in cells:
        c.status = CellStatus.INACTIVE
    return False

def print_cell_status(cells):
    print([{"value": c.value, "group id": c.group.group_id, "group status": c.group.status, "cell status": c.status, "left": c.left_boundary, "right": c.right_boundary} for c in cells])


def activate(cells, cell_groups):
    for cell in cells:
        cell.start()
    
    for group in cell_groups:
        group.start()


def get_pass_in_args(argv):
    cell_type = ""
    try:
        opts, args = getopt.getopt(argv, "h", ["cell_type="])
    except getopt.GetoptError:
        print("please specify cell type using '--cell_type='")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("multithread_cell_sorting.py --cell_type=<cell_type>")
            sys.exit()
        
        if opt == "--cell_type":
            cell_type = arg

    if not cell_type:
        print("please specify cell type using '--cell_type='")
        sys.exit(2)
    
    return cell_type

def kill_all_thread(cells, groups):
    for c in cells:
        c.status = CellStatus.INACTIVE
    
    for g in groups:
        g.status = GroupStatus.MERGED

def is_sorted(cells):
    prev_cell = cells[0]
    for c in cells:
        if c.value < prev_cell.value:
            return False
        prev_cell = c
    return True

def prepare_sorting_list():
    # return [i for i in range(100)]
    res = []
    for i in range(10):
        for j in range(20):
            res.append(i)
    return res

def main(argv):
    sorting_list = prepare_sorting_list()
    # print(sorting_list)
    for i in range(100):
        random.shuffle(sorting_list)
        sorting_steps_for_each_run = []
        threadLock = threading.Lock()
        status_probe = StatusProbe()
        print(f">>>>>>>>>>>>>>>>> Prepare cells to sort for experiment {i} <<<<<<<<<<<<<<<<<<<<")
        random.shuffle(sorting_list)

        cells, cell_groups = create_cell_groups_based_on_value_list(sorting_list, threadLock, status_probe, 100, False, True, True)
        threadLock.acquire()
        print("Activating cells...")
        activate(cells, cell_groups)
        threadLock.release()

        print("Start sorting......")
        while not is_sorted(cells):
            # print_cell_status(cells)
            time.sleep(0.0001)
        threadLock.acquire()
        kill_all_thread(cells, cell_groups)
        threadLock.release()
        print(">>>>>>>>>>>>>>>>> Sorting complete, killed all threads. <<<<<<<<<<<<<<<<<<<<\n")
        #print(status_probe.cell_types[0])
        np.save(f'csv/cell_type_aggregation_random_dist_200_tests_bubble_selection_dup/exp_{i}', status_probe.cell_types)
        np.save(f'csv/cell_type_aggregation_random_dist_200_tests_bubble_selection_dup/exp_{i}_sorting_steps', status_probe.sorting_steps)
        
        # np.save(f'csv/cell_type_aggregation_random_dist_100_tests_selection_insertion/exp_{i}', status_probe.cell_types)
        # np.save(f'csv/cell_type_aggregation_random_dist_100_tests_selection_insertion/exp_{i}_sorting_steps', status_probe.sorting_steps)

        # np.save(f'csv/cell_type_aggregation_random_dist_100_tests_selection_insertion_dup/exp_{i}', status_probe.cell_types)
        # np.save(f'csv/cell_type_aggregation_random_dist_100_tests_selection_insertion_dup/exp_{i}_sorting_steps', status_probe.sorting_steps)
        
        # np.save(f'csv/cell_type_aggregation_random_dist_100_tests_bubble_insertion_dup/exp_{i}', status_probe.cell_types)
        # np.save(f'csv/cell_type_aggregation_random_dist_100_tests_bubble_insertion_dup/exp_{i}_sorting_steps', status_probe.sorting_steps)
        
        
        # np.save(f'csv/cell_type_aggregation_random_dist_100_tests_bubble_bubble_bubble/exp_{i}', status_probe.cell_types)
        # np.save(f'csv/cell_type_aggregation_random_dist_100_tests_bubble_bubble_bubble/exp_{i}_sorting_steps', status_probe.sorting_steps)

if __name__ == "__main__":
    main(sys.argv[1:])