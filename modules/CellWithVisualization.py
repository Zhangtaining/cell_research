class CellWithVisualization:
    def __init__(self, value, current_position):
        self.value = value
        self.current_position = current_position
        self.target_position = current_position
        self.cell = None
        self.is_moving = False
        self.right_neighbor = None
        self.left_neighbor = None

    def plot_cell(self, ax):
        self.cell = ax.text(
            self.current_position[0],
            self.current_position[1],
            f"{self.value[0]}",
            size=10,
            ha="center", va="center",
            bbox=dict(
                boxstyle="circle, pad=0.5",
                fc=(1., 1-0.01 * self.value[0],
                1-0.01 * self.value[0])
            )
        )

    def move(self):
        if abs(self.target_position[0] - self.current_position[0]) < 0.00001:
            self.is_moving = False
            self.current_position = self.target_position
        else:
            f = 1 if self.target_position[0] > self.current_position[0] else -1
            self.current_position = (
                self.current_position[0] + f * 0.1, self.current_position[1])
        self.cell.set_position(self.current_position)

    def move_to_right(self):
        self.target_position = (self.current_position[0] + 1.0, self.current_position[1])
        self.is_moving = True
        self.right_neighbor.target_position = (
            self.right_neighbor.current_position[0] - 1.0,
            self.right_neighbor.current_position[1]
        )
        self.right_neighbor.is_moving = True 
        right = self.right_neighbor

        self.right_neighbor = right.right_neighbor
        if right.right_neighbor:
            right.right_neighbor.left_neighbor = self

        right.left_neighbor = self.left_neighbor
        if self.left_neighbor:
            self.left_neighbor.right_neighbor = right

        right.right_neighbor = self 
        self.left_neighbor = right

    def get_cell_value(self):
        if len(self.value) == 1:
            return self.value[0]
        
    def get_cell_x_value(self):
        return self.value[0]

    def get_cell_y_value(self):
        return self.value[1]

    def should_move_to_right(self, compare_method=None):
        if not self.right_neighbor:
            return False
        if len(self.value) == 1:
            return self.get_cell_value() > self.right_neighbor.get_cell_value() 
        
        if len(self.value) == 2:
            x = self.get_cell_x_value()
            y = self.get_cell_y_value()
            right_x = self.right_neighbor.get_cell_x_value()
            right_y = self.right_neighbor.get_cell_y_value()
            if not compare_method:
                return x*x + y*y > right_x*right_x + right_y*right_y
            if compare_method == 'x first':
                if x > right_x:
                    return True
                if x == right_x and y > right_y:
                    return True
            if compare_method == 'y first':
                if y > right_y:
                    return True
                if y > right_y == x > right_x:
                    return True

    
