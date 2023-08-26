import numpy as np
import matplotlib.pyplot as plt
from matplotlib.text import Text
from matplotlib.animation import FuncAnimation, PillowWriter
import time
import sys
from modules.CellWithVisualization import CellWithVisualization


VALUE_LIST = [[28], [34], [6], [20], [7], [89], [34], [18], [29], [51]]

fig, ax = plt.subplots()

plt.xlim(0, 12)
plt.ylim(0, 3)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

cells = []
prev_cell = CellWithVisualization(VALUE_LIST[0], (1, 1.5))
cells.append(prev_cell)
for i in range(1, len(VALUE_LIST)):
    cell = CellWithVisualization(VALUE_LIST[i], (i + 1, 1.5))
    prev_cell.right_neighbor = cell
    cell.left_neighbor = prev_cell
    cells.append(cell)
    prev_cell = cell

for cell in cells:
    cell.plot_cell(ax)

def update(_, cs):
    cells_in_moving = [cell for cell in cs if cell.is_moving]

    if cells_in_moving:
        for cell in cells_in_moving:
            cell.move()
        return cs 
    
    for cell in cs:
        if cell.should_move_to_right():
            cell.move_to_right()
            return cs
    

ani = FuncAnimation(fig, update, 300, fargs=([cells]), interval=50, blit=False)
f = "visual_gifs/cell_sorting_1d.gif"
writergif = PillowWriter(fps=30) 
ani.save(f, writer=writergif)
plt.show()