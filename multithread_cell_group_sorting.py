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


VALUE_LIST = [28, 34, 6, 20, 7, 89, 34, 18, 29, 51]
#VALUE_LIST = range(20,0,-1)

def create_cell_groups_based_on_value_list(value_list, threadLock, canvas):
    if len(value_list) == 0:
        return []
    cells = []
    cell_groups = []
    cell_images = []
    group_images = []
    for i in range(0, len(value_list)):
        cell = None
        # if cell_type == "selection":
        #     cell = SelectionSortCell(i + 1, VALUE_LIST[i], threadLock, i, cells, 0, len(VALUE_LIST) - 1)
        # if cell_type == "bubble":
        # let's assume all the group cells have the same sorting logic.
        if random.random() < 0.5:
            cell = BubbleSortCell(i + 1, VALUE_LIST[i], threadLock, (i, 1), cells, (i, 1), (i, 1), StatusProbe(), disable_visualization=True)
        else:
            cell = SelectionSortCell(i + 1, VALUE_LIST[i], threadLock, (i, 1), cells, (i, 1), (i, 1), StatusProbe(), disable_visualization=True)
        period = random.randint(100, 200)
        start_count_down = random.randint(0, period)
        cell_group = CellGroup([cell], cells, i, (i, 1), (i, 1), GroupStatus.SLEEP, threadLock, start_count_down, period)
        cell.group = cell_group
        cell_image = CellImage(canvas, cell)
        group_image = CellGroupImage(canvas, cell_group)

        cell_images.append(cell_image)
        group_images.append(group_image)

        if cell and cell_group:
            cells.append(cell)
            cell_groups.append(cell_group)

    return cells, cell_groups, cell_images, group_images

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

def main(argv):
    window = Tk()
    window.title("Cell Sorting With Sleeping Cycle")

    canvas = Canvas(window, width=500, height=500,)
    canvas.pack()
    window.update()
    #cell_type = get_pass_in_args(argv)
    threadLock = threading.Lock()
    cells, cell_groups, cell_images, group_images = create_cell_groups_based_on_value_list(VALUE_LIST, threadLock, canvas)
    threadLock.acquire()
    activate(cells, cell_groups)
    threadLock.release()

    # shape = canvas.create_oval(30 - 20, 30 - 20, 30 + 20, 30 + 20, fill="white")
    # text = canvas.create_text(30, 30, text="3")

    while True:
        # check_cell_status(cells)
        for image in cell_images:
            image.move()

        for group_image in group_images:
            group_image.update_shape()
        window.update()
        time.sleep(0.0001)

    window.mainloop()


if __name__ == "__main__":
    main(sys.argv[1:])