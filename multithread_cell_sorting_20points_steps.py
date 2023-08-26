import sys, getopt
from tkinter import * 
import threading
import time
from modules.multithread.StatusProbe import StatusProbe
from modules.multithread.SelectionSortCell import SelectionSortCell
from modules.multithread.BubbleSortCell import BubbleSortCell
from modules.multithread.MergeSortCell import MergeSortCell
from modules.multithread.CellGroup import CellGroup, GroupStatus
from modules.multithread.MultiThreadCell import CellStatus
from visualization.CellImage import CellImage
from visualization.CellGroupImage import CellGroupImage
import random
import numpy as np


# VALUE_LIST = [28, 34, 6, 20, 7, 89, 34, 18, 29, 51]
#VALUE_LIST = range(20,0,-1)

def create_cells_within_one_group(value_list, threadLock, status_probe, bubble_sort_percentage):
    if len(value_list) == 0:
        return []
    left_boundary = (0, 1)
    right_boundary = (len(value_list) - 1, 1)
    cells = []
    for i in range(0, len(value_list)):
        cell = None
        if random.random() <= bubble_sort_percentage:
            cell = BubbleSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, left_boundary, right_boundary, status_probe, disable_visualization=True)
        else:
            cell = SelectionSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, left_boundary, right_boundary, status_probe, disable_visualization=True)
        cells.append(cell)

    period = 100000000
    start_count_down = 1000000
    cell_group = CellGroup(cells, cells, 0, left_boundary, right_boundary, GroupStatus.ACTIVE, threadLock, start_count_down, period)
    for cell in cells:
        cell.group = cell_group 
    # cells[random.randint(0, len(cells) - 1 )].set_cell_to_freeze()
    return cells, [cell_group]

def print_current_status(cells):
    print([{"value": c.value, "group id": c.group.group_id, "group status": c.group.status, "cell status": c.status, "left": c.left_boundary, "right": c.right_boundary, "ideal position": c.ideal_position} for c in cells])

def is_sorted(cells):
    prev_cell = cells[0]
    for c in cells:
        if c.value < prev_cell.value:
            return False
        prev_cell = c
    return True
    # print([{"value": c.value, "group id": c.group.group_id, "group status": c.group.status, "cell status": c.status, "left": c.left_boundary, "right": c.right_boundary} for c in cells])

def kill_all_thread(cells, groups):
    for c in cells:
        c.status = CellStatus.INACTIVE
    
    for g in groups:
        g.status = GroupStatus.MERGED

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

def main(argv):
    #cell_type = get_pass_in_args(argv)
    sorting_list = [i for i in range(10)]
    sorting_steps_for_each_run_bubble = []
    sorting_steps_for_each_run_selection = []
    for i in range(20):
        threadLock = threading.Lock()
        random.shuffle(sorting_list)
        print(f">>>>>>>>>>>>>>>>> Prepare cells to sort for bubble experiment {i + 1} <<<<<<<<<<<<<<<<<<<<")
        status_probe = StatusProbe()
        cells, cell_groups = create_cells_within_one_group(sorting_list, threadLock, status_probe, 1)
        threadLock.acquire()
        print("Activating cells...")
        activate(cells, cell_groups)
        threadLock.release()

        # shape = canvas.create_oval(30 - 20, 30 - 20, 30 + 20, 30 + 20, fill="white")
        # text = canvas.create_text(30, 30, text="3")

        print("Start sorting......")
        while not is_sorted(cells):
            # print_current_status(cells)
            time.sleep(0.0001)
        threadLock.acquire()
        kill_all_thread(cells, cell_groups)
        threadLock.release()
        sorting_steps_for_each_run_bubble.append(status_probe.sorting_steps)
        print(">>>>>>>>>>>>>>>>> Sorting complete, killed all threads. <<<<<<<<<<<<<<<<<<<<\n")
        time.sleep(2)

        print(f">>>>>>>>>>>>>>>>> Prepare cells to sort for selection experiment {i + 1} <<<<<<<<<<<<<<<<<<<<")
        status_probe = StatusProbe()
        cells, cell_groups = create_cells_within_one_group(sorting_list, threadLock, status_probe, 0)
        threadLock.acquire()
        print("Activating cells...")
        activate(cells, cell_groups)
        threadLock.release()

        # shape = canvas.create_oval(30 - 20, 30 - 20, 30 + 20, 30 + 20, fill="white")
        # text = canvas.create_text(30, 30, text="3")

        print("Start sorting......")
        while not is_sorted(cells):
            # print_current_status(cells)
            time.sleep(0.0001)
        threadLock.acquire()
        kill_all_thread(cells, cell_groups)
        threadLock.release()
        sorting_steps_for_each_run_selection.append(status_probe.sorting_steps)
        print(">>>>>>>>>>>>>>>>> Sorting complete, killed all threads. <<<<<<<<<<<<<<<<<<<<\n")
        time.sleep(2)
    
    sorting_process_steps_bubble = np.array(sorting_steps_for_each_run_bubble)
    np.save('csv/bubble_sort_20_points_sorting_steps', sorting_process_steps_bubble)

    sorting_process_steps_selection = np.array(sorting_steps_for_each_run_selection)
    np.save('csv/selection_sort_20_points_sorting_steps', sorting_process_steps_selection)


if __name__ == "__main__":
    main(sys.argv[1:])