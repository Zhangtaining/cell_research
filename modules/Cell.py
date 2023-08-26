class Cell:
    def __init__(self, value, current_position):
        self.value = value
        self.current_position = current_position
        self.target_position = current_position
        self.cell = None
        self.is_moving = False
        self.left_neighbor = None 
        self.right_neighbor = None

    def move_to_right(self):
        if not self.right_neighbor:
            return 

        right = self.right_neighbor

        self.right_neighbor = right.right_neighbor
        if right.right_neighbor is not None:
            right.right_neighbor.left_neighbor = self

        right.left_neighbor = self.left_neighbor
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

    
