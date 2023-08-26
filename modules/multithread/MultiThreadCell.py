import threading
import time
from .StatusProbe import StatusProbe
from enum import Enum


class CellStatus(Enum):
    ACTIVE = 1
    SLEEP = 2
    MERGE = 3
    MOVING = 4
    INACTIVE = 5
    ERROR = 6
    FREEZE = 7


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
        status_probe,
        cell_vision=1,
        disable_visualization=False,
        swapping_count=[0],
        export_steps=[],
        reverse_direction=False
    ):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.value = value
        self.tried_to_swap_with_frozen = False
        self.current_position = current_position
        self.target_position = current_position
        self.cells = cells
        self.lock = lock
        self.left_boundary = left_boundary
        self.right_boundary = right_boundary
        self.cell_vision = cell_vision
        self.status = CellStatus.ACTIVE
        self.previous_status = CellStatus.ACTIVE
        self.read_error= False
        self.ideal_position = None
        self.visualization_disabled = disable_visualization
        self.swapping_count = swapping_count
        self.export_steps = export_steps
        self.status_probe = status_probe
        self.cell_type_dict = {
            'Bubble': 0,
            'Selection': 1,
            'Insertion': 2
        }
        self.reverse_direction=reverse_direction
        self.with_lock = False
        
    def take_snapshot(self):
        return [c.value for c in self.cells], [[c.group.group_id, self.cell_type_dict[c.cell_type] if c.label == 0 else c.label, c.value, 1 if c.status == CellStatus.FREEZE else 0] for c in self.cells]
    
    def get_current_snapshot(self):
        return {"value": self.value, "group id": self.group.group_id, "group status": self.group.status, "cell status": self.status, "left": self.left_boundary, "right": self.right_boundary, "cell_type": self.cell_type, "should_move": self.should_move(), "with_lock": self.with_lock}

    def set_cell_to_freeze(self):
        self.status = CellStatus.FREEZE
        self.previous_status = CellStatus.FREEZE

    def swap(self, target_position, skip_stats=False):
        current_cell_at_target = self.cells[int(target_position[0])]
        if self.status == CellStatus.FREEZE:
            # or current_cell_at_target.status == CellStatus.FREEZE
            if not self.tried_to_swap_with_frozen:
                self.status_probe.count_frozen_cell_attempt()
                self.tried_to_swap_with_frozen = True
            return
        self.tried_to_swap_with_frozen = False 
        current_cell_at_target.tried_to_swap_with_frozen = False
        self.status = CellStatus.MOVING
        current_cell_at_target.status = CellStatus.MOVING
        self.cells[self.current_position[0]] = current_cell_at_target
        self.cells[target_position[0]] = self
        current_cell_at_target.target_position = self.current_position
        self.target_position = target_position
        if self.visualization_disabled:
            self.current_position = self.target_position
            current_cell_at_target.current_position = current_cell_at_target.target_position
            self.status = self.previous_status
            current_cell_at_target.status = current_cell_at_target.previous_status
        if not skip_stats:
            self.swapping_count[0] = self.swapping_count[0] + 1
            self.status_probe.record_swap()
            snapshot, cell_type_snapshot = self.take_snapshot()
            self.status_probe.record_sorting_step(snapshot)
            self.export_steps.append(snapshot)
            self.status_probe.record_cell_type(cell_type_snapshot)

    def update(self):
        pass

    
    def move(self):
        pass


    def should_move(self):
        pass

    def run(self):
        while self.status != CellStatus.INACTIVE:
            self.move()