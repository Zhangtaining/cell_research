
import threading
import time

class MultiThreadCell(threading.Thread):
    def __init__(self, threadID, value, lock, start_ptr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.value = value
        self.left_neighbor = None 
        self.right_neighbor = None 
        self.lock = lock
        self.start_ptr = start_ptr

    def get_values_as_arr(self):
        p = self.start_ptr.right_neighbor
        values = []
        while p:
            values.append(p.value)
            p = p.right_neighbor
        return values

    def print_current_list(self):
        self.lock.acquire()
        values = self.get_values_as_arr()
        print(values)
        self.lock.release()
    
    def move(self):
        if self.right_neighbor is not None and self.value > self.right_neighbor.value:
            #self.lock.acquire()
            if not self.right_neighbor:
                return 

            right = self.right_neighbor

            self.right_neighbor = right.right_neighbor
            if right.right_neighbor is not None:
                right.right_neighbor.left_neighbor = self

            right.left_neighbor = self.left_neighbor
            if self.left_neighbor is not None:
                self.left_neighbor.right_neighbor = right

            right.right_neighbor = self 
            self.left_neighbor = right
            #self.lock.release()

    def run(self):
        while True:
            self.move()
                #self.print_current_list()

    
