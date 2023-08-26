import threading
import time
from .MultiThreadCell import MultiThreadCell, CellStatus
from enum import Enum

class GroupStatus(Enum):
    ACTIVE = 1
    MERGING = 2
    SLEEP = 3
    MERGED = 4


class CellGroup(threading.Thread):
    def __init__(
        self,
        cells_in_group,
        global_cells,
        group_id,
        left_boundary,
        right_boundary,
        status,
        lock,
        count_down,
        phase_period
    ):
        threading.Thread.__init__(self)
        self.group_id = group_id
        self.cells_in_group = cells_in_group
        self.global_cells = global_cells
        self.left_boundary_position = left_boundary
        self.right_boundary_position = right_boundary
        self.status = status
        self.lock = lock
        self.phase_period = phase_period
        self.count_down = count_down

    def is_group_sorted(self):
        prev_cell = self.global_cells[self.left_boundary_position[0]]
        for i in range(self.left_boundary_position[0], self.right_boundary_position[0] + 1):
            cell = self.global_cells[i]
            if cell.status == CellStatus.SLEEP or cell.status == CellStatus.MOVING or cell.value < prev_cell.value:
                return False
            prev_cell = cell 
        return True

    def is_boundary(self):
        checking_next_index = self.current_position + 1
        return checking_next_index >= len(self.global_cells) or self.group_id != self.global_cells[checking_next_index].group_id

    def find_next_group(self):
        if self.right_boundary_position[0] + 1 < len(self.global_cells):
            return self.global_cells[self.right_boundary_position[0] + 1].group
        return None

    def merge_with_group(self, next_group):
        next_group.status = GroupStatus.MERGED 
        self.count_down = min(self.count_down, next_group.count_down)
        self.phase_period = min(self.phase_period, next_group.phase_period)
        self.right_boundary_position = next_group.right_boundary_position
        self.cells_in_group.extend(next_group.cells_in_group)
        buuble_cell_cnt = 0
        selection_cell_cnt = 0
        for cell in self.cells_in_group:
            cell.group = self 
            cell.left_boundary = self.left_boundary_position 
            cell.right_boundary = self.right_boundary_position
            cell.update()
            if cell.cell_type == 'Insertion':
                cell.enable_to_move = False 
        for cell in self.cells_in_group:
            if cell.cell_type == 'Insertion':
                cell.enable_to_move = False
                break
        
    def all_cells_inactive(self):
        for c in self.cells_in_group:
            if c.status != CellStatus.INACTIVE:
                return False 
        return True

    def change_status(self):
        self.count_down = self.phase_period
        if self.status == GroupStatus.ACTIVE:
            self.status = GroupStatus.SLEEP
            self.put_cells_to_sleep()
            return 
        
        if self.status == GroupStatus.SLEEP:
            self.status = GroupStatus.ACTIVE
            self.awake_cells()
            return 

    def put_cells_to_sleep(self):
        for cell in self.cells_in_group:
            if cell.status != CellStatus.MOVING and cell.status != CellStatus.INACTIVE:
                cell.status = CellStatus.SLEEP
    
    def awake_cells(self):
        for cell in self.cells_in_group:
            if cell.status != CellStatus.INACTIVE:
                cell.status = cell.previous_status


    def run(self):
        while self.status != GroupStatus.MERGED and not self.all_cells_inactive():
            if self.count_down == 0:
                self.change_status()
 
            if self.status == GroupStatus.SLEEP:
                self.put_cells_to_sleep()
                self.count_down -= 1
                time.sleep(0.05)

            if self.status == GroupStatus.ACTIVE:
                self.lock.acquire()
                if self.status == GroupStatus.ACTIVE and self.is_group_sorted():
                    next_group = self.find_next_group()
                    if next_group and next_group.status == GroupStatus.ACTIVE and next_group.is_group_sorted():
                        self.merge_with_group(next_group)
                self.lock.release()
                time.sleep(0.05)
                self.count_down -= 1
