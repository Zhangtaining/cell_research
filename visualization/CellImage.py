from modules.multithread.MultiThreadCell import CellStatus
import random

class CellImage:
    def __init__(self, canvas, cell):
        self.canvas = canvas
        self.cell = cell
        self.create_image()
        self.velocity = 0.5

    
    def create_image(self):
        (x, y) = self.position_on_graph(self.cell.current_position)
        r = 10
        shape = self.canvas.create_oval(x - r, y - r, x + r, y + r)
        text = self.canvas.create_text(x, y, text=f"{self.cell.value}")
        self.shape = shape
        self.text = text


    def position_on_graph(self, pos):
        return (pos[0] * 40 + 50, pos[1] * 40 + 200) 


    def get_cell_background(self):
        if self.cell.cell_type == 'Bubble':
            return 'green'
        if self.cell.cell_type == 'Selection':
            return 'blue'


    def move(self):
        v_x = 0
        v_y = 0
        if self.cell.read_error:
            self.canvas.itemconfig(self.shape, fill="red")
        # else:
        #     self.canvas.itemconfig(self.shape, fill="white")

        if self.cell.status == CellStatus.SLEEP:
            self.canvas.itemconfig(self.shape, fill="grey")
        elif self.cell.read_error:
            self.canvas.itemconfig(self.shape, fill="red")
        else:
            self.canvas.itemconfig(self.shape, fill=self.get_cell_background())

        if self.cell.status == CellStatus.MOVING:
            self.canvas.itemconfig(self.shape, fill=self.get_cell_background())
            target_position = self.position_on_graph(self.cell.target_position)      
            current_position = self.get_cordinator()
            v_x = self.get_moving_speed(current_position[0], target_position[0])
            v_y = self.get_moving_speed(current_position[1], target_position[1])

            if v_x == 0 and v_y == 0:
                self.cell.status = self.cell.previous_status
                self.cell.current_position = self.cell.target_position

        self.canvas.move(self.shape, v_x, v_y)
        self.canvas.move(self.text, v_x, v_y)


    def get_moving_speed(self, c, t):
        if abs(t - c) < 0.00001:
            return 0

        if t < c:
            return -1 * self.velocity
        
        return self.velocity


    def get_cordinator(self):
        return self.canvas.coords(self.text)