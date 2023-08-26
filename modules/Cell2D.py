class Cell_2D:
    def __init__(self, value, current_position):
        self.value = value
        self.current_position = current_position
        self.target_position = current_position
        self.cell = None
        self.compare_mode='eudian'
        self.is_moving = False
        self.neighbors = []

    def plot_cell(self, ax):
        self.cell = ax.text(self.current_position[0], self.current_position[1], f"{self.value}", size=10,
            ha="center", va="center",
            bbox=dict(boxstyle="circle, pad=0.5", fc=(1., 1-0.01 * self.value , 1-0.01 * self.value))
            )

    def _moving_direction(self):
        if self.target_position[0] == self.current_position[0]:
            return 1
        delta_x =  self.target_position[0] - self.current_position[0]
        delta_y = self.target_position[1] - self.current_position[1]
        return delta_y / delta_x

    def _arrive_target_position(self):
        return abs(self.target_position[0] - self.current_position[0]) < 0.00001 and abs(self.target_position[1] - self.current_position[1]) < 0.00001

    def move_on_graph(self):
        if self._arrive_target_position() :
            self.is_moving = False
            self.current_position = self.target_position
        else:
            f = 1 if self.target_position[0] > self.current_position[0] else -1
            delta_step_on_x = f * self.moving_step
            delta_step_on_y = f * self.moving_step * self._moving_direction()
            if self.target_position[0] == self.current_position[0]:
                f = 1 if self.target_position[1] > self.current_position[1] else -1
                delta_step_on_x = 0
                delta_step_on_y = f * self.moving_step * self._moving_direction()
            self.current_position = (self.current_position[0] + delta_step_on_x, self.current_position[1]+ delta_step_on_y)
        self.cell.set_position(self.current_position)

    def get_moving_steps(self):
        if self.current_position[0] == self.target_position[0]:
            return abs(self.target_position[1] - self.current_position[1]) / 10.0

        return abs(self.target_position[0] - self.current_position[0]) / 10.0

    def move(self, neighbor):
        self.target_position = neighbor.current_position 
        neighbor.target_position = self.current_position
        self.is_moving = True
        self.moving_step = self.get_moving_steps()
        neighbor.is_moving = True
        neighbor.moving_step = neighbor.get_moving_steps()

    def get_cell_value(self):
        if len(self.value) == 1:
            return self.value[0]
        
    def get_cell_x_value(self):
        return self.value[0]

    def get_cell_y_value(self):
        return self.value[1]

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
        if compare_mode == 'eudian':
            return (neighbor.current_position[0] - self.current_position[0]) ** 2 + (neighbor.current_position[1] - self.current_position[1]) ** 2

    def get_far_away_neighbors(self):
        return [n for n in self.neighbors if n.get_absolute_distance() > self.get_absolute_distance()]

    def get_closer_neighbors(self):
        return [n for n in self.neighbors if n.get_absolute_distance() < self.get_absolute_distance()]

    def should_move(self, compare_method=None):
        far_away_neighbors = self.get_far_away_neighbors()
        closer_neighbors = self.get_closer_neighbors()
        for n in far_away_neighbors:
            if n.value < self.value:
                self.move(n)
                return True
        for n in closer_neighbors:
            if n.value > self.value:
                self.move(n)
                return True
        return False

    
