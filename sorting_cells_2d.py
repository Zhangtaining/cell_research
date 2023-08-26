import sys
from modules.Cell import Cell

VALUE_LIST = [[28, 4], [34, 16], [6, 32], [5, 20], [7, 99], [89, 3], [1, 34], [35, 18], [49, 29], [26, 51]]

def create_cells_based_on_value_list(value_list):
    if len(value_list) == 0:
        return []
    cells = []
    start_ptr = Cell(-1)
    current_cell = Cell(value_list[0])
    start_ptr.right_neighbor = current_cell
    current_cell.left_neighbor = start_ptr
    cells.append(current_cell)
    for i in range(1, len(value_list)):
        cell = Cell(value_list[i])
        cells.append(cell)
        cell.left_neighbor = current_cell
        current_cell.right_neighbor = cell 
        current_cell = cell

    return cells, start_ptr 

def get_values_as_arr(start_ptr):
    p = start_ptr.right_neighbor
    values = []
    while p:
        values.append(p.value)
        p = p.right_neighbor
    return values

def print_current_list(start_ptr):
    values = get_values_as_arr(start_ptr)
    print(values)

def sort_cells(cells, start_ptr):
    need_to_sort = True 
    step = 1
    while need_to_sort:
        need_to_sort = False 
        for cell in cells:
            if cell.should_move_to_right(compare_method='y first'):
                need_to_sort = True
                cell.move_to_right()
                print(f"Step {step}: ")
                print_current_list(start_ptr)
                step += 1
                # We start from only allow 1 cell move each time.
                # TODO: make this multi thread to allow cells moving
                # at the same time.
                break 

def get_total_disorder(start_ptr):
    x_disorder = get_current_monotonicity(get_values_as_arr(start_ptr), 0)
    y_disorder = get_current_monotonicity(get_values_as_arr(start_ptr), 1)
    return x_disorder + y_disorder

def sort_cells_with_global_view(cells, start_ptr):
    need_to_sort = True 
    step = 1
    current_total_disorder = get_total_disorder(start_ptr)
    while need_to_sort:
        need_to_sort = False 
        for cell in cells:
            cell.move_to_right()
            total_disorder_after_move = get_total_disorder(start_ptr)
            if total_disorder_after_move >= current_total_disorder:
                cell.left_neighbor.move_to_right()
            else:
                eed_to_sort = True
                print(f"Step {step}: ")
                print_current_list(start_ptr)
                current_total_disorder = total_disorder_after_move
                step += 1
                break

def get_current_monotonicity(arr, index):
        monotonicity_value = 0
        prev = arr[0][index]
        for i in range(1, len(arr)):
            if arr[i][index] < prev:
                monotonicity_value += 1
            prev = arr[i][index]
        return monotonicity_value

def main(argv):
    cells, start_ptr = create_cells_based_on_value_list(VALUE_LIST)
    sort_cells_with_global_view(cells, start_ptr)
    print(f'Disorder for x: {get_current_monotonicity(get_values_as_arr(start_ptr), 0)}')
    print(f'Disorder for y: {get_current_monotonicity(get_values_as_arr(start_ptr), 1)}')

if __name__ == "__main__":
    main(sys.argv[1:])