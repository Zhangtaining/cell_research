
import threading
import time
from .MultiThreadCell import MultiThreadCell, CellStatus
from .CellGroup import GroupStatus
import random

class InsertionSortCell(MultiThreadCell):
    def __init__(self, threadID, value, lock, current_position, cells, left_boundary, right_boundary, status_probe, disable_visualization=False, swapping_count=[0], export_steps=[], label=0, reverse_direction=False):
        super().__init__(threadID, value, lock, current_position, cells, left_boundary, right_boundary, status_probe, disable_visualization=disable_visualization, swapping_count=swapping_count, export_steps=export_steps, reverse_direction=reverse_direction)
        self.cell_vision = 1
        self.cell_type = 'Insertion'
        self.label = label

    def within_boundary(self, pos):
        if pos[0] > self.right_boundary[0] or pos[1] > self.right_boundary[1]:
            return False
        
        if pos[0] < self.left_boundary[0] or pos[1] < self.left_boundary[1]:
            return False

        return True

    def should_move(self):
        if self.reverse_direction:
            bigger_than_left = False
            if self.current_position[0] > self.left_boundary[0]:
                bigger_than_left = self.value > self.cells[int(self.current_position[0] - 1)].value and self.cells[int(self.current_position[0] - 1)].status ==  CellStatus.ACTIVE 
            
            return self.is_enable_to_move() and bigger_than_left
            #return bigger_than_left
        
        smaller_than_left = False
        if self.current_position[0] > self.left_boundary[0]:
            smaller_than_left = self.value < self.cells[int(self.current_position[0] - 1)].value and self.cells[int(self.current_position[0] - 1)].status ==  CellStatus.ACTIVE 
            
        return self.is_enable_to_move() and smaller_than_left
        #return smaller_than_left

    def should_move_to(self, target_position):
        if (
            (self.status == CellStatus.ACTIVE or self.status == CellStatus.FREEZE)
            and self.within_boundary(target_position)
            and (self.cells[int(target_position[0])].status == CellStatus.ACTIVE  or self.cells[int(target_position[0])].status == CellStatus.FREEZE)
        ):
            next_cell = int(target_position[0])
            while next_cell < len(self.cells) and self.cells[next_cell].status ==  CellStatus.FREEZE:
                next_cell += 1
            # if self.status == CellStatus.FREEZE:
            #     print("xxxxxxxxxxxxxxx1")

            # if self.cells[int(target_position[0])].status == CellStatus.FREEZE:
            #     print("xxxxxxxxxxxxxxx2")
            err_happen = random.random() < 0
            if err_happen:
                return not self.value > self.cells[int(target_position[0])].value 
            # if self.cells[int(target_position[0])].status == CellStatus.FREEZE:
            #     print("xxxxxxxxxxxxxxx3")
            if self.reverse_direction:
                return self.value > self.cells[int(target_position[0])].value
            return self.value < self.cells[int(target_position[0])].value
        # else:
        #     if not self.within_boundary(target_position):
        #         print(target_position)
        #     if self.within_boundary(target_position):
        #         print(self.status)
        
    def is_enable_to_move(self):
        if self.reverse_direction:
            prev = 100000
        else:
            prev = -1
        for i in range(int(self.left_boundary[0]), int(self.current_position[0])):
            if self.cells[i].status == CellStatus.FREEZE:
                prev = -1
                continue
            if self.reverse_direction and self.cells[i].value > prev:
                return False
            
            if not self.reverse_direction and self.cells[i].value < prev:
                return False
            prev = self.cells[i].value
        return True
    
    def move(self):
        self.lock.acquire()
        if not self.is_enable_to_move():
            self.lock.release()
            return
        
        if self.should_move():
            self.status_probe.record_compare_and_swap()
        
        if self.group.status == GroupStatus.SLEEP and self.status != CellStatus.MOVING:
            self.status = CellStatus.SLEEP
        target_position = (self.current_position[0] - self.cell_vision, self.current_position[1])
        # if self.status == CellStatus.FREEZE:
        #         print("xxxxxxxxxxxxxxx4")
        if self.should_move_to(target_position):
            self.swap(target_position)
        self.lock.release()

