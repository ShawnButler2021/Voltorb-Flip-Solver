class VoltorbFlip:
    def __init__(self, row_hints, col_hints):
        self.size = 5
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.row_hints = row_hints
        self.col_hints = col_hints

    def is_valid(self):
        # Check row hints
        for i in range(self.size):
            if sum(1 for x in self.board[i] if x == 'V') != self.row_hints[i]:
                return False
        
        # Check column hints
        for j in range(self.size):
            if sum(1 for i in range(self.size) if self.board[i][j] == 'V') != self.col_hints[j]:
                return False
        
        return True

    def backtrack(self, row=0, col=0):
        # If we reached the end of the board, check validity
        if row == self.size:
            return self.is_valid()
        
        # Move to the next cell
        next_row, next_col = (row, col + 1) if col < self.size - 1 else (row + 1, 0)

        # Try placing a Voltorb
        self.board[row][col] = 'V'
        if self.backtrack(next_row, next_col):
            return True

        # Try placing numbers 1, 2, or 3
        for num in [1, 2, 3]:
            self.board[row][col] = num
            if self.backtrack(next_row, next_col):
                return True

        # Backtrack
        self.board[row][col] = None
        return False

    def solve(self):
        if self.backtrack():
            return self.board
        else:
            return None


# Example hints (number of Voltorbs per row and column)
row_hints = [1, 2, 1, 0, 1]  # Example hints for rows
col_hints = [1, 1, 2, 1, 0]  # Example hints for columns

# Create a Voltorb Flip instance and solve it
voltorb_flip_solver = VoltorbFlip(row_hints, col_hints)
solution = voltorb_flip_solver.solve()

# Output the solution
if solution:
    for row in solution:
        print(row)
else:
    print("No solution found.")

