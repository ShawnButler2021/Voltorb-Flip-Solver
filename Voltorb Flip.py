Python 3.11.5 (tags/v3.11.5:cce6ba9, Aug 24 2023, 14:38:34) [MSC v.1936 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import heapq

class Cell:
    def __init__(self, x, y, value=None):
        self.x = x
        self.y = y
        self.value = value  # 2, 3, or -1 for Voltorb
        self.is_flipped = False  # Flag to check if this cell has been flipped

class State:
    def __init__(self, grid, score, path):
        self.grid = grid  # The game grid
        self.score = score  # Current score
        self.path = path  # Path of revealed cells

def heuristic(state):
    # Estimate the number of unrevealed 2s and 3s
    return sum(1 for row in state.grid for cell in row if cell.value in {2, 3} and not cell.is_flipped)

def get_neighbors(state):
    # Generate possible next states from the current state
    neighbors = []
    for row in range(len(state.grid)):
        for col in range(len(state.grid[0])):
            cell = state.grid[row][col]
            if not cell.is_flipped and cell.value in {2, 3}:
                # Create a new grid with the cell flipped
                new_grid = [r[:] for r in state.grid]  # Copy the grid
                new_grid[row][col].is_flipped = True  # Mark the cell as flipped
                new_score = state.score + cell.value
                new_path = state.path + [(row, col)]
                neighbors.append(State(new_grid, new_score, new_path))
    return neighbors

def is_goal_state(state):
    # Check if all 2s and 3s have been flipped
    return all(cell.is_flipped or cell.value == -1 for row in state.grid for cell in row if cell.value in {2, 3})

def a_star(start_state):
    open_set = []
    closed_set = set()

    heapq.heappush(open_set, (start_state.score + heuristic(start_state), start_state))

    while open_set:
        # Extract node with the smallest f(n)
        _, current_state = heapq.heappop(open_set)

        # If all 2s and 3s are flipped, return the current state
if is_goal_state(current_state):
return current_state  # Return the goal state

closed_set.add(tuple(map(tuple, [(cell.value if cell.is_flipped else None) for cell in row] for row in current_state.grid)))

for neighbor in get_neighbors(current_state):
# Insert or update neighbor in the priority queue
neighbor_tuple = tuple(map(tuple, [(cell.value if cell.is_flipped else None) for cell in row] for row in neighbor.grid))
if neighbor_tuple in closed_set:
continue  # Ignore closed states

# Insert the neighbor into the priority queue
heapq.heappush(open_set, (neighbor.score + heuristic(neighbor), neighbor))
return None  # No solution found

