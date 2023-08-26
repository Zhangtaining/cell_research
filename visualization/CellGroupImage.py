from modules.multithread.CellGroup import GroupStatus
from PIL import Image, ImageDraw, ImageTk


class CellGroupImage:
    def __init__(self, canvas, cell_group):
        self.canvas = canvas
        self.cell_group = cell_group
        self.offset = 19
        self.create_image()

    
    def create_image(self):
        right_boundary = self.cell_group.right_boundary_position
        top_left = self.get_top_left_point(self.position_on_graph(self.cell_group.left_boundary_position))
        bottom_right = self.get_bottom_right_point(self.position_on_graph(self.cell_group.right_boundary_position))
        shape = self.create_round_rectangle(top_left[0], top_left[1], bottom_right[0], bottom_right[1])
        self.shape = shape


    def create_round_rectangle(self, x1, y1, x2, y2, radius=25):
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        return self.canvas.create_polygon(points, smooth=True, outline='red', fill='')

    def position_on_graph(self, pos):
        return (pos[0] * 40 + 50, pos[1] * 40 + 200) 

    def get_top_left_point(self, left_boundary_pos):
        return (left_boundary_pos[0] - self.offset, left_boundary_pos[1] - self.offset)


    def get_bottom_right_point(self, right_boundary_pos):
        return (right_boundary_pos[0] + self.offset, right_boundary_pos[1] + self.offset)


    def update_shape(self):
        self.canvas.delete(self.shape)
        if self.cell_group.status != GroupStatus.MERGED:
            self.create_image()