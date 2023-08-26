
import threading
import time
from .MultiThreadCell import MultiThreadCell, CellStatus
from .CellGroup import GroupStatus
import random

class BubbleSortCell(MultiThreadCell):
    def __init__(self, threadID, value, lock, current_position, cells, left_boundary, right_boundary, status_probe, disable_visualization=False, swapping_count=[0], export_steps=[], label=0, reverse_direction=False):
        super().__init__(threadID, value, lock, current_position, cells, left_boundary, right_boundary, status_probe, disable_visualization=disable_visualization, swapping_count=swapping_count, export_steps=export_steps, reverse_direction=reverse_direction)
        self.cell_vision = 1
        self.cell_type = 'Bubble'
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
            smaller_than_right = False 
            if self.current_position[0] < self.right_boundary[0]:
                smaller_than_right = self.value < self.cells[int(self.current_position[0] + 1)].value and  self.cells[int(self.current_position[0] + 1)].status ==  CellStatus.ACTIVE
            
            return  bigger_than_left or  smaller_than_right
        
        smaller_than_left = False
        if self.current_position[0] > self.left_boundary[0]:
            smaller_than_left = self.value < self.cells[int(self.current_position[0] - 1)].value and self.cells[int(self.current_position[0] - 1)].status ==  CellStatus.ACTIVE 
        bigger_than_right = False 
        if self.current_position[0] < self.right_boundary[0]:
            bigger_than_right = self.value > self.cells[int(self.current_position[0] + 1)].value and  self.cells[int(self.current_position[0] + 1)].status ==  CellStatus.ACTIVE
            
        return smaller_than_left or bigger_than_right

    def should_move_to(self, target_position, check_right):
            
        if (
            self.status == CellStatus.ACTIVE
            and self.within_boundary(target_position)
            and (self.cells[int(target_position[0])].status == CellStatus.ACTIVE  or self.cells[int(target_position[0])].status == CellStatus.FREEZE)
        ):
            err_happen = random.random() < 0
            if err_happen:
                return not self.value > self.cells[int(target_position[0])].value 
            if self.reverse_direction:
                return self.value < self.cells[int(target_position[0])].value if check_right else self.value > self.cells[int(target_position[0])].value
            return self.value > self.cells[int(target_position[0])].value if check_right else self.value < self.cells[int(target_position[0])].value
    
    def move(self):
        self.lock.acquire()
        self.with_lock = True
        if self.group.status == GroupStatus.SLEEP and self.status != CellStatus.MOVING:
            self.status = CellStatus.SLEEP
        if self.should_move():
            self.status_probe.record_compare_and_swap()
        # new logic - random check left or right
        check_right = random.random() < 0.5
        if check_right:
            target_position = (self.current_position[0] + self.cell_vision, self.current_position[1])
        else:
            target_position = (self.current_position[0] - self.cell_vision, self.current_position[1])
        if self.should_move_to(target_position, check_right):
            self.swap(target_position)
        self.lock.release()
        self.with_lock = False

