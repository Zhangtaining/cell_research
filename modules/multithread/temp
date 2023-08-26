import threading
import time
from enum import Enum

class CellStatus(Enum):
    ACTIVE = 1
    SLEEP = 2
    MERGE = 3
    MOVING = 4
    INACTIVE = 5

class MultiThreadCell(threading.Thread):
    def __init__(
        self,
        threadID,
        value,
        lock,
        current_position,
        cells,
        left_boundary,
        right_boundary,
        ax=None,
        cell_vision=1,
    ):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.value = value
        self.current_position = current_position
        self.target_position = current_position
        self.cells = cells
        self.lock = lock
        self.left_boundary = left_boundary
        self.right_boundary = right_boundary
        self.cell_vision = cell_vision
        self.status = CellStatus.ACTIVE
        if ax:
            self.cell_graph = ax.text(
                self.current_position,
                1, # Default 1D y value
                f"{self.value}",
                size=10,
                ha="center", va="center",
                bbox=dict(
                    boxstyle="circle, pad=0.5",
                    fc=(1., 1-0.01 * self.value[0],
                    1-0.01 * self.value[0])
                )
            )

    def swap(self, target_position):
        current_cell_at_target = self.cells[target_position]
        self.cells[self.current_position] = current_cell_at_target
        current_cell_at_target.target_position = self.current_position
        self.cells[target_position] = self
        self.target_position = target_position
        # self.status = CellStatus.MOVING
        # current_cell_at_target.status = CellStatus.MOVING
        self.current_position = self.current_position
        current_cell_at_target.current_position = current_cell_at_target.target_position

    def move_on_graph(self):
        if abs(self.target_position - self.current_position) < 0.00001:
            self.status = CellStatus.ACTIVE
            self.current_position = self.target_position
        else:
            f = 1 if self.target_position > self.current_position else -1
            self.current_position = self.current_position + f * 0.1
        self.cell.set_position(self.current_position, 1)

    def update(self):
        if self.status == CellStatus.MOVING:
            self.move_on_graph()

    
    def move(self):
        pass

    def run(self):
        while self.status != CellStatus.INACTIVE:
            self.move()



import sys, getopt
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.text import Text
from matplotlib.animation import FuncAnimation
from modules.multithread.SelectionSortCell import SelectionSortCell
from modules.multithread.BubbleSortCell import BubbleSortCell
from modules.multithread.MergeSortCell import MergeSortCell
from modules.multithread.CellGroup import CellGroup, GroupStatus
from modules.multithread.MultiThreadCell import CellStatus


VALUE_LIST = [28, 34, 6, 20, 7, 89, 34, 18, 29, 51]
#VALUE_LIST = range(20,0,-1)

def create_cell_groups_based_on_value_list(value_list, threadLock, ax):
    if len(value_list) == 0:
        return []
    cells = []
    cell_groups = []
    for i in range(0, len(value_list)):
        cell = None
        # if cell_type == "selection":
        #     cell = SelectionSortCell(i + 1, VALUE_LIST[i], threadLock, i, cells, 0, len(VALUE_LIST) - 1)
        # if cell_type == "bubble":
        # let's assume all the group cells have the same sorting logic.
        cell = BubbleSortCell(i + 1, VALUE_LIST[i], threadLock, i, cells, i, i)
        cell_group = CellGroup([cell], cells, i, i, i, GroupStatus.ACTIVE, threadLock)
        cell.group = cell_group


        if cell and cell_group:
            cells.append(cell)
            cell_groups.append(cell_group)

    return cells, cell_groups

def check_cell_status(cells):
    print([c.value for c in cells])
    prev_cell = cells[0]
    for c in cells:
        if c.value < prev_cell.value:
            return 
        prev_cell = c
    
    for c in cells:
        c.status = CellStatus.INACTIVE
    #print([{"value": c.value, "group id": c.group.group_id, "status": c.group.status, "left": c.left_boundary, "right": c.right_boundary} for c in cells])


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
    fig, ax = plt.subplots()

    plt.xlim(0, 12)
    plt.ylim(0, 3)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    #cell_type = get_pass_in_args(argv)
    threadLock = threading.Lock()
    cells, cell_groups = create_cell_groups_based_on_value_list(VALUE_LIST, threadLock, None)
    threadLock.acquire()
    activate(cells, cell_groups)
    threadLock.release()
    while True:
        check_cell_status(cells)
        time.sleep(0.0001)
        

if __name__ == "__main__":
    main(sys.argv[1:])
    
