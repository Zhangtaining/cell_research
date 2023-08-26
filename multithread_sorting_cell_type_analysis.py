import sys, getopt
from tkinter import * 
import threading
import time
from modules.multithread.SelectionSortCell import SelectionSortCell
from modules.multithread.BubbleSortCell import BubbleSortCell
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

def create_cell_groups_based_on_value_list(value_list, threadLock, status_probe):
    if len(value_list) == 0:
        return []
    cells = []
    cell_groups = []
    cell_type_list = get_cell_type_list(len(value_list), True, 0.5)
    create_bubble_cell = True
    for i in range(0, len(value_list)):
        cell = None
        create_bubble_cell = cell_type_list[i]
        if create_bubble_cell:
            cell = BubbleSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, (i, 1), (i, 1), status_probe, disable_visualization=True)
        else:
            cell = SelectionSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, (i, 1), (i, 1), status_probe, disable_visualization=True)
        period = random.randint(100, 200)
        start_count_down = random.randint(0, period)
        cell_group = CellGroup([cell], cells, i, (i, 1), (i, 1), GroupStatus.SLEEP, threadLock, start_count_down, period)
        cell.group = cell_group

        if cell and cell_group:
            cells.append(cell)
            cell_groups.append(cell_group)
    # cells[random.randint(0, len(cells) - 1 )].set_cell_to_freeze()

    return cells, cell_groups

def check_cell_status(cells):
    print([c.value for c in cells])
    prev_cell = cells[0]
    for c in cells:
        if c.value < prev_cell.value:
            return True
        prev_cell = c
    
    for c in cells:
        c.status = CellStatus.INACTIVE
    return False
    # print([{"value": c.value, "group id": c.group.group_id, "group status": c.group.status, "cell status": c.status, "left": c.left_boundary, "right": c.right_boundary} for c in cells])


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

def main(argv):
    for i in range(1000):
        sorting_list = [n for n in range(100)]
        sorting_steps_for_each_run = []
        threadLock = threading.Lock()
        status_probe = StatusProbe()
        print(f">>>>>>>>>>>>>>>>> Prepare cells to sort for experiment {i} <<<<<<<<<<<<<<<<<<<<")
        random.shuffle(sorting_list)

        cells, cell_groups = create_cell_groups_based_on_value_list(sorting_list, threadLock, status_probe)
        threadLock.acquire()
        print("Activating cells...")
        activate(cells, cell_groups)
        threadLock.release()

        print("Start sorting......")
        while not is_sorted(cells):
            #print_current_status(cells)
            time.sleep(0.0001)
        threadLock.acquire()
        kill_all_thread(cells, cell_groups)
        threadLock.release()
        print(">>>>>>>>>>>>>>>>> Sorting complete, killed all threads. <<<<<<<<<<<<<<<<<<<<\n")
        #print(status_probe.cell_types[0])
        np.save(f'csv/cell_type_with_group_id_random_dist_1000_tests/exp_{i}', status_probe.cell_types)


if __name__ == "__main__":
    main(sys.argv[1:])