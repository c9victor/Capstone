# https://gist.github.com/lvngd/8c1aafc4851985bbd239bc59153f26f9
# https://lvngd.com/blog/generating-and-solving-sudoku-puzzles-python/

from random import shuffle
import copy


"""
SudokuGenerator
input: grid can be a 2-D matrix of a Sudoku puzzle to solve, or None to generate a new puzzle.
"""


class SudokuGenerator:
    """generates and solves Sudoku puzzles using a backtracking algorithm"""

    def __init__(self, grid=None):
        self.counter = 0
        self.grid = [[0 for i in range(9)] for j in range(9)]
        self.full_grid = [[0 for i in range(9)] for j in range(9)]
        self.generate_five()
        """
        if grid:
            if len(grid[0]) == 9 and len(grid) == 9:
                self.grid = grid
                self.original = copy.deepcopy(grid)
                self.generate_puzzle()
            else:
                print("input needs to be a 9x9 matrix")
        else:
            self.grid = [[0 for i in range(9)] for j in range(9)]
            self.generate_puzzle()
            self.original = copy.deepcopy(self.grid)
        """

    def generate_five (self):
        self.generate_puzzle() 
        grid0 = self.full_grid
        grid1 = [[0 for i in range(9)] for j in range(9)]
        grid2 = [[0 for i in range(9)] for j in range(9)]
        grid3 = [[0 for i in range(9)] for j in range(9)]
        grid4 = [[0 for i in range(9)] for j in range(9)]
        for i in range(6, 9):
            for j in range(6, 9):
                grid1[i][j] = grid0[i-6][j-6] 
        #self.print_grid('grid0', grid=grid0)
        #self.print_grid('grid1', grid=grid1)
        for i in range(6, 9): 
            for j in range(0, 3): 
                grid2[i][j] = grid0[i-6][j+6] 
        #self.print_grid('grid2', grid=grid2)
        ### TO DO ###
        for i in range(0, 3): 
            for j in range(0, 3): 
                grid3[i][j] = grid0[i+6][j+6] 
        #self.print_grid('grid3', grid=grid3)
        for i in range(0, 3): 
            for j in range(6, 9): 
                grid4[i][j] = grid0[i+6][j-6] 
        #self.print_grid('grid4', grid=grid4)
        print('grid1')
        self.generate_puzzle(grid1)
        print('grid2')
        self.generate_puzzle(grid2)
        print('grid3')
        self.generate_puzzle(grid3)
        print('grid4')
        self.generate_puzzle(grid4)
        '''
        self.print_grid('grid0', grid=self.grid)
        self.print_grid('grid1', grid=grid1)
        self.print_grid('grid2', grid=grid2)
        self.print_grid('grid3', grid=grid3)
        self.print_grid('grid4', grid=grid4)
        '''

    # generates a new puzzle and solves it
    def generate_puzzle(self, grid=None):
        if grid:
            self.generate_solution(grid)   
            self.print_grid(grid=grid)
            self.remove_numbers_from_grid(grid)
        else:
            self.generate_solution(self.grid) 
            self.print_grid('middle grid')
            self.full_grid = copy.deepcopy(self.grid)  #new code
            self.remove_numbers_from_grid(self.grid)
        #self.print_grid('full solution')
        #self.print_grid('with removed numbers') 
        return

    def print_grid(self, grid_name=None, grid=None):
        if grid_name:
            print(grid_name)
        if grid:
            for row in grid:
                print(row)
        else:
            for row in self.grid:
                print(row)
        return

    def test_sudoku(self, grid):
        # tests each square to make sure it is a valid puzzle
        for row in range(9):
            for col in range(9):
                num = grid[row][col]
                # remove number from grid to test if it's valid
                grid[row][col] = 0
                if not self.valid_location(grid, row, col, num):
                    return False
                else:
                    # put number back in grid
                    grid[row][col] = num
        return True

    def num_used_in_row(self, grid, row, number):
        """returns True if the number has been used in that row"""
        if number in grid[row]:
            return True
        return False

    def num_used_in_column(self, grid, col, number):
        """returns True if the number has been used in that column"""
        for i in range(9):
            if grid[i][col] == number:
                return True
        return False

    def num_used_in_subgrid(self, grid, row, col, number):
        """returns True if the number has been used in that subgrid/box"""
        sub_row = (row // 3) * 3
        sub_col = (col // 3) * 3
        for i in range(sub_row, (sub_row + 3)):
            for j in range(sub_col, (sub_col + 3)):
                if grid[i][j] == number:
                    return True
        return False

    def valid_location(self, grid, row, col, number):
        """return False if the number has been used in the row, column or subgrid"""
        if self.num_used_in_row(grid, row, number):
            return False
        elif self.num_used_in_column(grid, col, number):
            return False
        elif self.num_used_in_subgrid(grid, row, col, number):
            return False
        return True

    def find_empty_square(self, grid):
        """return the next empty square coordinates in the grid"""
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return

    def solve_puzzle(self, grid):
        """solve the sudoku puzzle with backtracking"""
        for i in range(0, 81):
            row = i//9
            col = i % 9
            # find next empty cell
            if grid[row][col] == 0:
                for number in range(1, 10):
                    # check that the number hasn't been used in the row/col/subgrid
                    if self.valid_location(grid, row, col, number):
                        grid[row][col] = number
                        if not self.find_empty_square(grid):
                            self.counter += 1
                            break
                        else:
                            if self.solve_puzzle(grid):
                                return True
                break
        grid[row][col] = 0
        return False

    def generate_solution(self, grid):
        """generates a full solution with backtracking"""
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(0, 81):
            row = i//9
            col = i % 9
            # find next empty cell
            if grid[row][col] == 0:
                shuffle(number_list)
                for number in number_list:
                    if self.valid_location(grid, row, col, number):
                        grid[row][col] = number
                        if not self.find_empty_square(grid):
                            return True
                        else:
                            if self.generate_solution(grid):
                                # if the grid is full
                                return True
                break
        grid[row][col] = 0
        return False

    def get_non_empty_squares(self, grid):
        """returns a shuffled list of non-empty squares in the puzzle"""
        non_empty_squares = []
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] != 0:
                    non_empty_squares.append((i, j))
        shuffle(non_empty_squares)
        return non_empty_squares

    def remove_numbers_from_grid(self, grid=None):
        """remove numbers from the grid to create the puzzle"""
        # get all non-empty squares from the grid
        non_empty_squares = self.get_non_empty_squares(grid)
        non_empty_squares_count = len(non_empty_squares)
        rounds = 3
        while rounds > 0 and non_empty_squares_count >= 17:
            # there should be at least 17 clues
            row, col = non_empty_squares.pop()
            non_empty_squares_count -= 1
            # might need to put the square value back if there is more than one solution
            removed_square = grid[row][col]
            grid[row][col] = 0
            # make a copy of the grid to solve
            grid_copy = copy.deepcopy(grid)
            # initialize solutions counter to zero
            self.counter = 0
            self.solve_puzzle(grid_copy)
            # if there is more than one solution, put the last removed cell back into the grid
            if self.counter != 1:
                grid[row][col] = removed_square
                non_empty_squares_count += 1
                rounds -= 1
        return


def main():
    solved = SudokuGenerator()


main()  
