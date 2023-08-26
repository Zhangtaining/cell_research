import threading
import time
from .MultiThreadCell import MultiThreadCell, CellStatus

class MergeSortCell(MultiThreadCell):
    def __init__(self, threadID, value, lock, current_position, cells):
        super().__init__(threadID, value, lock, current_position, cells)
        self.group_id = current_position
        self.status = CellStatus.ACTIVE

    def is_boundary(self):
        checking_next_index = self.current_position + 1
        return checking_next_index >= len(self.cells) or self.group_id != self.cells[checking_next_index].group_id

    def check_group_sorted(self):
        # We assume all cells have positive number as value
        prev_value = 0 
        for c in self.cells:
            if c.group_id == self.group_id:
                if c.value < prev_value:
                    return False 
                prev_value = c.value
        return True

        
    def move(self):
        # ========== ACTIVE Status ==========
        # If found other group to merge, 2 actions happen:
        #   1. change all cells' status in the 2 groups to MERGE
        #   2. change all cells' group id to the min(group1 id, group2 id)
        if self.status == CellStatus.ACTIVE and self.is_boundary():
            checking_index = self.current_position + 1
            if checking_index < len(self.cells):
                another_boundary_cell = self.cells[checking_index]
                if another_boundary_cell.status != CellStatus.ACTIVE:
                    return
                new_group_id = min(another_boundary_cell.group_id, self.group_id)
                current_group_ids = [another_boundary_cell.group_id, self.group_id]
                self.lock.acquire()
                for c in self.cells:
                    if c.group_id in current_group_ids:
                        c.status = CellStatus.MERGE
                        c.group_id = new_group_id
                self.lock.release()

        # ========== MERGE Status ==========
        # If the cell is at the group boundary. It need to check the whole group is sorted
        # If the whole group is sorted, then it need to change the status back to ACTIVE
        if self.status == CellStatus.MERGE:
            self.lock.acquire()
            if self.is_boundary() and self.check_group_sorted():
                for c in self.cells:
                    if c.group_id == self.group_id:
                        c.status = CellStatus.ACTIVE
                self.lock.release()
                return
            self.lock.release()
            
            target_position = self.current_position + 1
            if target_position < len(self.cells) and self.group_id == self.cells[target_position].group_id and self.value > self.cells[target_position].value:
                self.lock.acquire()
                self.swap(target_position)
                self.lock.release()
