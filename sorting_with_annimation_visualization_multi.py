import numpy as np
import matplotlib.pyplot as plt
from matplotlib.text import Text
import threading
from matplotlib.animation import FuncAnimation, PillowWriter
import time
import sys
from modules.multithread.MultiThreadCellForVisualize import MultiThreadCellForVisualize


VALUE_LIST = [28, 34, 6, 20, 7, 89, 34, 18, 29, 51]
threadLock = threading.Lock()

fig, ax = plt.subplots()

plt.xlim(0, 12)
plt.ylim(0, 3)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

cells = []
for i in range(0, len(VALUE_LIST)):
    cell = MultiThreadCellForVisualize(i, VALUE_LIST[i], threadLock, (i + 1, 1.5), 'x distance')
    cell.neighbors = cells
    cells.append(cell)

for cell in cells:
    cell.plot_cell(ax)

# def update(_, cs):
#     cells_in_moving = [cell for cell in cs if cell.is_moving]

#     if cells_in_moving:
#         for cell in cells_in_moving:
#             cell.move()
#         return cs 
    
#     for cell in cs:
#         if cell.should_move_to_right():
#             cell.move_to_right()
#             return cs

for cell in cells:
    cell.start()

plt.show()



# ani = FuncAnimation(fig, update, 300, fargs=([cells]), interval=50, blit=False)
# f = "visual_gifs/cell_sorting_1d.gif"
# writergif = PillowWriter(fps=30) 
# ani.save(f, writer=writergif)
