import sys, getopt
from tkinter import * 
import threading
import time
from modules.multithread.StatusProbe import StatusProbe
from modules.multithread.SelectionSortCell import SelectionSortCell
from modules.multithread.BubbleSortCell import BubbleSortCell
from modules.multithread.MergeSortCell import MergeSortCell
from modules.multithread.InsertionSortCell import InsertionSortCell
from modules.multithread.CellGroup import CellGroup, GroupStatus
from modules.multithread.MultiThreadCell import CellStatus
from visualization.CellImage import CellImage
from visualization.CellGroupImage import CellGroupImage
from analysis.utils import get_monotonicity
import random
import numpy as np


# VALUE_LIST = [28, 34, 6, 20, 7, 89, 34, 18, 29, 51]
#VALUE_LIST = range(20,0,-1)

def create_cells_within_one_group(value_list, threadLock, status_probe, cell_type, frozen_cell_number):
    if len(value_list) == 0:
        return []
    left_boundary = (0, 1)
    right_boundary = (len(value_list) - 1, 1)
    cells = []
    for i in range(0, len(value_list)):
        cell = None
        if cell_type == 'selection':
            cell = SelectionSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, left_boundary, right_boundary, status_probe, disable_visualization=True)
        if cell_type == 'bubble':
            cell = BubbleSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, left_boundary, right_boundary, status_probe, disable_visualization=True)
        if cell_type == 'insertion':
            cell = InsertionSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, left_boundary, right_boundary, status_probe, disable_visualization=True)
        # if random.random() <= bubble_sort_percentage:
        # cell = BubbleSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, left_boundary, right_boundary, status_probe, disable_visualization=True)
        # cell = InsertionSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, left_boundary, right_boundary, status_probe, disable_visualization=True)
        # else:
        #     cell = SelectionSortCell(i + 1, value_list[i], threadLock, (i, 1), cells, left_boundary, right_boundary, status_probe, disable_visualization=True)
        cells.append(cell)


    period = 1000000000
    start_count_down = 1000000000
    cell_group = CellGroup(cells, cells, 0, left_boundary, right_boundary, GroupStatus.ACTIVE, threadLock, start_count_down, period)
    for cell in cells:
        cell.group = cell_group 
    for i in range(frozen_cell_number):
        cells[random.randint(0, len(cells) - 1 )].set_cell_to_freeze()
    
    # if cell_type == 'insertion':
    #     for i in range(len(cells)):
    #         cell = cells[i]
    #         if cell.status != CellStatus.FREEZE:
    #             cell.enable_to_move = True
    #             break

    return cells, [cell_group]

def is_sorted(cells):
    prev_cell = cells[0]
    for c in cells:
        if c.value < prev_cell.value:
            return False
        prev_cell = c
    return True

def print_status(cells):
    print([{"value": c.value, "group id": c.group.group_id, "group status": c.group.status, "cell status": c.status, "left": c.left_boundary, "right": c.right_boundary} for c in cells])

def kill_all_thread(cells, groups):
    for c in cells:
        c.status = CellStatus.INACTIVE
    
    for g in groups:
        g.status = GroupStatus.MERGED

def activate(cells, cell_groups):
    for cell in cells:
        if cell.status != CellStatus.FREEZE:
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


def no_cells_should_move(cells):
    for c in cells:
        if c.status == CellStatus.SLEEP:
            return False
        if c.status == CellStatus.ACTIVE and c.should_move():
            return False 
    
    return True


def main(argv):
    #cell_type = get_pass_in_args(argv)
    for frozen_cell_num in [2, 3]:
        sorting_list = [i for i in range(100)]
        sorting_steps_for_each_run_bubble = []
        sorting_steps_for_each_run_selection = []
        sorting_steps_for_each_run_insertion = []
        sorting_frozen_swap_count_for_each_run_bubble = []
        sorting_cell_type_each_run_bubble = []
        sorting_frozen_swap_count_for_each_run_selection = []
        sorting_frozen_swap_count_for_each_run_insertion = []
        total_sorting_steps_for_bubble = []
        total_sorting_steps_for_selection = []
        total_sorting_steps_for_insertion = []
        for i in range(100):
            threadLock = threading.Lock()
            random.shuffle(sorting_list)
            print(f">>>>>>>>>>>>>>>>> Prepare cells to sort for bubble experiment {i + 1} <<<<<<<<<<<<<<<<<<<<")
            status_probe = StatusProbe()
            cells, cell_groups = create_cells_within_one_group(sorting_list, threadLock, status_probe, 'bubble', frozen_cell_num)
            #create_cells_within_one_group(sorting_list, threadLock, status_probe, 'bubble')
            threadLock.acquire()
            print("Activating cells...")
            activate(cells, cell_groups)
            threadLock.release()

            print("Start sorting......")
            while not no_cells_should_move(cells):
                time.sleep(1)
            threadLock.acquire()
            kill_all_thread(cells, cell_groups)
            threadLock.release()
            sorting_cell_type_each_run_bubble.append(status_probe.cell_types)
            sorting_steps_for_each_run_bubble.append(status_probe.sorting_steps)
            sorting_frozen_swap_count_for_each_run_bubble.append(status_probe.frozen_swap_attempts)
            total_sorting_steps_for_bubble.append(status_probe.compare_and_swap_count)
            print(">>>>>>>>>>>>>>>>> Sorting complete, killed all threads. <<<<<<<<<<<<<<<<<<<<\n")
            time.sleep(2)

            # print(f">>>>>>>>>>>>>>>>> Prepare cells to sort for selection experiment {i + 1} <<<<<<<<<<<<<<<<<<<<")
            # status_probe = StatusProbe()
            # cells, cell_groups = create_cells_within_one_group(sorting_list, threadLock, status_probe, 'selection', frozen_cell_num)
            # threadLock.acquire()
            # print("Activating cells...")
            # activate(cells, cell_groups)
            # threadLock.release()

            # # shape = canvas.create_oval(30 - 20, 30 - 20, 30 + 20, 30 + 20, fill="white")
            # # text = canvas.create_text(30, 30, text="3")

            # print("Start sorting......")
            # while not no_cells_should_move(cells):
            #     time.sleep(1)
            # threadLock.acquire()
            # kill_all_thread(cells, cell_groups)
            # threadLock.release()
            # sorting_steps_for_each_run_selection.append(status_probe.sorting_steps)
            # sorting_frozen_swap_count_for_each_run_selection.append(status_probe.frozen_swap_attempts)
            # total_sorting_steps_for_selection.append(status_probe.compare_and_swap_count)
            # print(">>>>>>>>>>>>>>>>> Sorting complete, killed all threads. <<<<<<<<<<<<<<<<<<<<\n")

            # print(f">>>>>>>>>>>>>>>>> Prepare cells to sort for insertion experiment {i + 1} <<<<<<<<<<<<<<<<<<<<")
            # status_probe = StatusProbe()
            # cells, cell_groups = create_cells_within_one_group(sorting_list, threadLock, status_probe, 'insertion', frozen_cell_num)
            # threadLock.acquire()
            # print("Activating cells...")
            # activate(cells, cell_groups)
            # threadLock.release()

            # shape = canvas.create_oval(30 - 20, 30 - 20, 30 + 20, 30 + 20, fill="white")
            # text = canvas.create_text(30, 30, text="3")

            # print("Start sorting......")
            # while not no_cells_should_move(cells):
            #     # time.sleep(1)
            #     continue

            # threadLock.acquire()
            # kill_all_thread(cells, cell_groups)
            # threadLock.release()
            # sorting_steps_for_each_run_insertion.append(status_probe.sorting_steps)
            # sorting_frozen_swap_count_for_each_run_insertion.append(status_probe.frozen_swap_attempts)
            # total_sorting_steps_for_insertion.append(status_probe.compare_and_swap_count)
            # if get_monotonicity(status_probe.sorting_steps[-1]) > 2:
            #     print(status_probe.sorting_steps[-1])
            # print(">>>>>>>>>>>>>>>>> Sorting complete, killed all threads. <<<<<<<<<<<<<<<<<<<<\n")
            # time.sleep(2)
        sorting_process_cell_types_buuble = np.array(sorting_cell_type_each_run_bubble, dtype=object)
        np.save(f'csv/bubble_sort_sorting_with_{frozen_cell_num}frozen_steps_cell_type_100exps', sorting_process_cell_types_buuble)
        #np.save(f'csv/bubble_sort_sorting_with_{frozen_cell_num}frozen_total_steps_100exps', total_sorting_steps_for_bubble)
        #np.save(f'csv/insertion_sort_sorting_with_{frozen_cell_num}frozen_total_steps_100exps', total_sorting_steps_for_insertion)
        #np.save(f'csv/selection_sort_sorting_with_{frozen_cell_num}frozen_total_steps_100exps', total_sorting_steps_for_selection)
        
        # sorting_process_steps_bubble = np.array(sorting_steps_for_each_run_bubble, dtype=object)
        # np.save(f'csv/bubble_sort_sorting_with_{frozen_cell_num}frozen_cannot_move_steps_100exps', sorting_process_steps_bubble)

        # sorting_process_steps_selection = np.array(sorting_steps_for_each_run_selection, dtype=object)
        # np.save(f'csv/selection_sort_sorting_with_{frozen_cell_num}frozen_cannot_move_steps_100exps', sorting_process_steps_selection)

        # sorting_process_steps_insertion = np.array(sorting_steps_for_each_run_insertion, dtype=object)
        # np.save(f'csv/insertion_sort_sorting_with_{frozen_cell_num}frozen_cannot_move_steps_100exps', sorting_process_steps_insertion)

        # sorting_frozen_swap_count_bubble = np.array(sorting_frozen_swap_count_for_each_run_bubble, dtype=object)
        # np.save(f'csv/bubble_sort_sorting_with_{frozen_cell_num}frozen_frozen_swap_count_100exps', sorting_frozen_swap_count_bubble)

        # sorting_frozen_swap_count_selection = np.array(sorting_frozen_swap_count_for_each_run_selection, dtype=object)
        # np.save(f'csv/selection_sort_sorting_with_{frozen_cell_num}frozen_frozen_swap_count_100exps', sorting_frozen_swap_count_selection)

        # sorting_frozen_swap_count_insertion = np.array(sorting_frozen_swap_count_for_each_run_insertion, dtype=object)
        # np.save(f'csv/insertion_sort_sorting_with_{frozen_cell_num}frozen_frozen_swap_count_100exps', sorting_frozen_swap_count_insertion)


if __name__ == "__main__":
    main(sys.argv[1:])