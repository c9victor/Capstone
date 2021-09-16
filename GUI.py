# GUI.py - RUN THIS FILE
import pygame
import random  # added by me
import csv  # added by me
import numpy as np  # added by me
from itertools import product  # needed for dlx implementation
from solver import solve, valid
import time
pygame.font.init()


class Grid:
    '''
    Opens a csv file filled with sudoku puzzles. The file contains two columns: starting puzzle and finished puzzle.
    The information in the starting puzzle column is parsed so that we can create a sudoku board.
    Note that the first line of the file contains headers, do not attempt to parse it as a puzzle
    '''
    with open('sudoku.csv', mode='r') as file:
        csvFile = csv.reader(file)
        puzzleNum = random.randint(1, 1000001)
        #print("Puzzle Number:", puzzleNum)
        puzzle = file.readlines()[puzzleNum]  
        file.close()  
    puzzle = puzzle.split(',')
    #print("Puzzle at start:", puzzle[0])  # start board
    #print("Finished puzzle:", puzzle[1])  # finished solution
    start_puzzle = list(puzzle[0])
    #print("list():", start_puzzle)
    start_puzzle = [int(numeric_string) for numeric_string in start_puzzle]  # https://www.codegrepper.com/code-examples/python/convert+string+array+to+int+array+python
    start_puzzle = np.reshape(start_puzzle, (9, 9))
    #print("reshape():\n", start_puzzle)
    board = start_puzzle

    
    ### For debugging purposes
    finish_puzzle = list(puzzle[1])
    finish_puzzle.pop()  # needed because there is a '\n' at the end of the list
    finish_puzzle = [int(numeric_string) for numeric_string in finish_puzzle]
    finish_puzzle = np.reshape(finish_puzzle, (9, 9))
    print("finished:\n", finish_puzzle)
    

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    '''
    New method. Used to reset the board when three mistakes are made or when dlx button is clicked.
    '''
    def reset(self):
        self.board = self.start_puzzle
        self.__init__(9, 9, 540, 540)

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    # new overloaded method for DLX deselect
    def clear(self, row, col):
        #if self.cubes[row][col].value == 0:
        self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos - position clicked
        :return: (row, col) - returns the row and col of the position clicked
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def dlx_solve_sudoku(self, size, grid):
        """ An efficient Sudoku solver using Algorithm X.
        
        >>> for solution in dlxSolve((3, 3), grid):
                print(*solution, sep='\\n')
        """
        R, C = size
        N = R * C
        X = ([("rc", rc) for rc in product(range(N), range(N))] +
            [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
            [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
            [("bn", bn) for bn in product(range(N), range(1, N + 1))])
        Y = dict()
        for r, c, n in product(range(N), range(N), range(1, N + 1)):
            b = (r // R) * R + (c // C) # Box number
            Y[(r, c, n)] = [
                ("rc", (r, c)),
                ("rn", (r, n)),
                ("cn", (c, n)),
                ("bn", (b, n))]
        
        ### test code
        #print("X ", X[0])
        #res = next(iter(Y))
        #print("The first key of dictionary is : " + str(res))

        X, Y = self.dlx_exact_cover(X, Y)
        for i, row in enumerate(grid):
            for j, n in enumerate(row):
                if n:
                    self.dlx_select(X, Y, (i, j, n))
        for solution in self.dlx_solve(X, Y, []):
            for (r, c, n) in solution:
                grid[r][c] = n
            yield grid

    def dlx_exact_cover(X, Y): #board.place(board.cubes[i][j].temp)
        X = {j: set() for j in X}
        for i, row in Y.items():
            for j in row:
                X[j].add(i)
        return X, Y

    def dlx_solve(self, X, Y, solution):
        if not X:
            yield list(solution)
        else:
            c = min(X, key=lambda c: len(X[c]))
            for r in list(X[c]):
                solution.append(r)
                cols = self.dlx_select(X, Y, r)
                self.board.place(self.board.cubes[r][c].temp)  # test
                for s in self.dlx_solve(X, Y, solution):
                    yield s
                self.dlx_deselect(X, Y, r, cols)
                self.clear(r, cols)  # test
                solution.pop()

    def dlx_select(X, Y, r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].remove(i)
            cols.append(X.pop(j))
        return cols

    def dlx_deselect(X, Y, r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j:
                        X[k].add(i)
### End Of Grid Class

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val
### End Of Cube Class

def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 200, 750))
    # Draw Strikes
    text = fnt.render(str(strikes), 1, (255, 0, 0))
    win.blit(text, (20, 750))

    #experimental code
    button_top = 600
    button_height = 30
    pygame.draw.rect(win, (216, 191, 216), [120, button_top, 170, button_height])  # (surface, (r, g, b), [left, top, width, height]) 
    text = fnt.render('New Puzzle' , True , (0, 0, 0))
    win.blit(text, (120, button_top))
    pygame.draw.rect(win, (216, 191, 216), [120, button_top + 50, 375, button_height])  # (surface, (r, g, b), [left, top, width, height]) 
    text = fnt.render('Watch Dancing Links Do It!' , True , (0, 0, 0))
    win.blit(text, (120, button_top + 50))

    # Draw grid and board
    board.draw(win)


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    #win = pygame.display.set_mode((540,600))  # (x,y)
    win = pygame.display.set_mode((540,800))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:
        if strikes == 3:
            print("3 Mistakes! Board Resetting...")
            board.reset()
            strikes = 0

        # play_time was encapsulated into this if statement so that when the puzzle is solved the time stops
        if not board.is_finished():
            play_time = round(time.time() - start) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            #run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # (x, y) of mouse position
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
                elif 120 <= pos[0] <= 495 and 650 <= pos[1] <= 680:
                    board.reset()
                    #yielded = [board.dlx_solve_sudoku((3, 3), board.board)]
                    print("DLX Button Clicked!!!")
                    board.dlx_solve_sudoku((3, 3), board.board)
                    #for solution in board.dlx_solve_sudoku((3, 3), board.board):
                    #    print("solved")
                    #    print(solution)
                    #print(yielded)


        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
