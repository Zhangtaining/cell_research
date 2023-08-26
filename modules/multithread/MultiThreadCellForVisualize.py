
import threading
import time

class MultiThreadCellForVisualize(threading.Thread):
    def __init__(self, threadID, value, lock, current_position, compare_mode):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.value = value
        self.neighbors = []
        self.lock = lock
        self.cell = None
        self.current_position = current_position
        self.compare_mode = compare_mode

    def plot_cell(self, ax):
        self.cell = ax.text(self.current_position[0], self.current_position[1], f"{self.value}", size=10,
            ha="center", va="center",
            bbox=dict(boxstyle="circle, pad=0.5", fc=(1., 1-0.01 * self.value , 1-0.01 * self.value))
            )

    def get_x_level_distance(self):
        return self.current_position[0]

    def get_y_level_distance(self):
        return self.current_position[1]

    def get_absolute_distance(self):
        if self.compare_mode == 'eudian':
            return self.current_position[0]**2 + self.current_position[1]**2

        if self.compare_mode == 'x distance':
            return self.get_x_level_distance()

        if self.compare_mode == 'y distance':
            return self.get_y_level_distance()
        return 0

    def get_neighbor_relative_distance(self, neighbor):
        if self.compare_mode == 'eudian':
            return (neighbor.current_position[0] - self.current_position[0]) ** 2 + (neighbor.current_position[1] - self.current_position[1]) ** 2
    
        if self.compare_mode == 'x distance':
            return abs(neighbor.current_position[0] - self.current_position[0])

    def _get_nearest_right_neighbor(self):
        min_distance = 9999999
        nearest_neighbor = None
        for n in self.neighbors:
            if n != self and self.get_neighbor_relative_distance(n) < min_distance:
                min_distance = self.get_neighbor_relative_distance(n)
                nearest_neighbor = n
        return nearest_neighbor
    
    def move(self):
        neighbor = self._get_nearest_right_neighbor()
        if neighbor and neighbor.value < self.value:
            current_position = self.current_position
            self.current_position = neighbor.current_position
            neighbor.current_position = current_position
            neighbor.cell.set_position(neighbor.current_position)
            self.cell.set_position(self.current_position)

    def print_cells(self):
        for c in self.neighbors:
            print(f'cell at {c.current_position} has value {c.value}')

    def run(self):
        while True:
            self.move()
            #self.print_cells()
                #self.print_current_list()

    
