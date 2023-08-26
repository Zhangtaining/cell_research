class StatusProbe:
    def __init__(self):
        self.sorting_steps = []
        self.swap_count = 0
        self.cell_types = []
        self.frozen_swap_attempts = 0
        self.compare_and_swap_count = 0

    def record_swap(self):
        self.swap_count += 1
        
    def record_compare_and_swap(self):
        self.compare_and_swap_count += 1

    def record_sorting_step(self, snapshot):
        self.sorting_steps.append(snapshot)
    
    def record_cell_type(self, snapshot):
        self.cell_types.append(snapshot)
    
    def count_frozen_cell_attempt(self):
        self.frozen_swap_attempts += 1
