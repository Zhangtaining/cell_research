import numpy as np
import matplotlib.pyplot as plt
from matplotlib.text import Text
from matplotlib.animation import FuncAnimation, PillowWriter
import time
import sys
from modules.Cell2D import Cell_2D


VALUE_LIST = [28, 34, 6, 20, 7, 89, 34, 18, 51, 29]
POSITION_LIST = [[0, 2], [1, 1], [2, 4], [1, 5], [6, 2], [3, 4], [2.5, 6], [4.3, 2], [2, 3], [4, 6]]
COMPARE_MODE = 'eudian'

circle1 = plt.Circle((0, 0), 1, color=(0.5, 1, 0.5), fill=False, linestyle='--')
circle2 = plt.Circle((0, 0), 2, color=(1, 0.5, 1), fill=False, linestyle='--')
circle3 = plt.Circle((0, 0), 3, color=(0.5, 1, 0.5), fill=False, linestyle='--')
circle4 = plt.Circle((0, 0), 4, color=(1, 0.5, 1), fill=False, linestyle='--')
circle5 = plt.Circle((0, 0), 5, color=(0.5, 1, 0.5), fill=False, linestyle='--')
circle6 = plt.Circle((0, 0), 6, color=(1, 0.5, 1), fill=False, linestyle='--')
circle7 = plt.Circle((0, 0), 7, color=(0.5, 1, 0.5), fill=False, linestyle='--')
circle8 = plt.Circle((0, 0), 8, color=(1, 0.5, 1), fill=False, linestyle='--')
circle9 = plt.Circle((0, 0), 9, color=(0.5, 1, 0.5), fill=False, linestyle='--')
circle10 = plt.Circle((0, 0), 10, color=(1, 0.5, 1), fill=False, linestyle='--')

fig, ax = plt.subplots()

plt.xlim(0, 8)
plt.ylim(0, 8)
plt.gca().set_aspect('equal', adjustable='box')
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.add_patch(circle1)
ax.add_patch(circle2)
ax.add_patch(circle3)
ax.add_patch(circle4)
ax.add_patch(circle5)
ax.add_patch(circle6)
ax.add_patch(circle7)
ax.add_patch(circle8)
ax.add_patch(circle9)
ax.add_patch(circle10)

cells = []
for i in range(0, len(VALUE_LIST)):
    cell = Cell_2D(VALUE_LIST[i], POSITION_LIST[i])
    cell.neighbors = cells
    cell.compare_mode = COMPARE_MODE
    cells.append(cell)

for cell in cells:
    cell.plot_cell(ax)

def update(_, cs):
    cells_in_moving = [cell for cell in cs if cell.is_moving]

    if cells_in_moving:
        for cell in cells_in_moving:
            cell.move_on_graph()
        return cs 
    
    for cell in cs:
        if cell.should_move():
            return cs
    
ani = FuncAnimation(fig, update, 400, fargs=([cells]), interval=1000, blit=False)
# f = f"visual_gifs/cell_sorting_2d_{COMPARE_MODE}.gif"
# writergif = PillowWriter(fps=30) 
# ani.save(f, writer=writergif)
plt.show()