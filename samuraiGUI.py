# GUI.py - RUN THIS FILE
import puzzle_retriever
from SudokuSolver import *
from puzzle_retriever import getPuzzle
import pygame
from itertools import product  # needed for dlx implementation
from solver import solve, valid
import time

pygame.font.init()


class Grid:
    board = puzzle_retriever.getPuzzle(1)

    board1 = [[0, 5, 1, 0, 6, 7, 2, 0, 8, 0, 0, 0, 9, 0, 8, 5, 6, 0, 7, 2, 0],
              [8, 7, 0, 0, 3, 0, 0, 0, 5, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 5, 3],
              [6, 0, 0, 0, 0, 8, 7, 0, 0, 0, 0, 0, 0, 0, 6, 4, 0, 0, 0, 0, 1],
              [0, 1, 8, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 2, 8, 0],
              [5, 2, 7, 0, 1, 0, 8, 4, 6, 0, 0, 0, 8, 3, 5, 0, 9, 0, 4, 1, 7],
              [0, 0, 0, 8, 0, 0, 1, 7, 0, 0, 0, 0, 0, 6, 4, 0, 0, 1, 0, 0, 0],
              [0, 0, 3, 6, 0, 0, 0, 0, 7, 0, 5, 0, 6, 0, 0, 0, 0, 5, 3, 0, 0],
              [2, 0, 0, 0, 8, 0, 0, 5, 9, 0, 6, 0, 1, 4, 0, 0, 3, 0, 0, 0, 5],
              [7, 0, 5, 3, 2, 0, 6, 8, 0, 9, 0, 4, 0, 7, 3, 0, 2, 9, 1, 0, 8],
              [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 6, 0, 9, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0],
              [9, 0, 6, 3, 4, 0, 5, 7, 0, 6, 0, 3, 0, 2, 1, 0, 3, 5, 7, 0, 8],
              [4, 0, 0, 0, 1, 0, 0, 6, 2, 0, 8, 0, 4, 3, 0, 0, 1, 0, 0, 0, 5],
              [0, 0, 2, 6, 0, 0, 0, 0, 3, 0, 9, 0, 8, 0, 0, 0, 0, 4, 3, 0, 0],
              [0, 0, 0, 2, 0, 0, 4, 9, 0, 0, 0, 0, 0, 7, 5, 0, 0, 2, 0, 0, 0],
              [6, 9, 1, 0, 3, 0, 2, 5, 7, 0, 0, 0, 3, 1, 4, 0, 6, 0, 5, 8, 2],
              [0, 7, 4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 4, 6, 0],
              [1, 0, 0, 0, 0, 5, 3, 0, 0, 0, 0, 0, 0, 0, 3, 7, 0, 0, 0, 0, 4],
              [7, 4, 0, 0, 2, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 7, 3],
              [0, 2, 8, 0, 6, 3, 7, 0, 9, 0, 0, 0, 7, 0, 2, 1, 4, 0, 9, 5, 0]]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def new_puzzle(self, diff):
        self.board = puzzle_retriever.getPuzzle(diff)

    def reset(self, samurai):
        if samurai:
            self.board = self.board1
            self.__init__(21, 21, 540, 540)
        else:
            self.board = self.board
            self.__init__(9, 9, 540, 540)

    def set_puzzle(self, puzzle):
        self.board = puzzle
        self.__init__(9, 9, 540, 540)

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win, samurai):
        if not samurai:
            # Draw Grid Lines
            gap = self.width / 9
            for i in range(self.rows + 1):
                if i % 3 == 0 and i != 0:
                    thick = 4
                else:
                    thick = 1
                pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
                pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

            # Draw Cubes
            for i in range(self.rows):
                for j in range(self.cols):
                    self.cubes[i][j].draw(win, samurai)

            # Draw Grid Lines
        else:
            gap = self.width / 27
            for i in range(10):
                if i % 3 == 0 and i != 0:
                    thick = 4
                else:
                    thick = 1
                # first grid
                pygame.draw.line(win, (0, 0, 0), (0, i * gap), (180, i * gap), thick)
                pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, 180), thick)

            for j in range(10):
                if j % 3 == 0 and j != 0:
                    thick = 4
                else:
                    thick = 1
                pygame.draw.line(win, (0, 0, 0), (120, 120 + (j * gap)), (300, 120 + (j * gap)), thick)
                pygame.draw.line(win, (0, 0, 0), (120 + (j * gap), 120), (120 + (j * gap), 300), thick)

            for z in range(10):
                if z % 3 == 0 and z != 0:
                    thick = 4
                else:
                    thick = 1
                pygame.draw.line(win, (0, 0, 0), (240, 240 + (z * gap)), (420, 240 + (z * gap)), thick)
                pygame.draw.line(win, (0, 0, 0), (240 + (z * gap), 240), (240 + (z * gap), 420), thick)

            for h in range(10):
                if h % 3 == 0 and h != 0:
                    thick = 4
                else:
                    thick = 1
                pygame.draw.line(win, (0, 0, 0), (240, h * gap), (420, h * gap), thick)
                pygame.draw.line(win, (0, 0, 0), (240 + (h * gap), 0), (240 + (h * gap), 180), thick)

            for a in range(10):
                if a % 3 == 0 and a != 0:
                    thick = 4
                else:
                    thick = 1
                pygame.draw.line(win, (0, 0, 0), (a * gap, 240), (a * gap, 420), thick)
                pygame.draw.line(win, (0, 0, 0), (0, 240 + (a * gap)), (180, 240 + (a * gap)), thick)

            # Draw Cubes
            for i in range(self.rows):
                for j in range(self.cols):
                    self.cubes[i][j].draw(win, samurai)

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

    def click(self, pos, samurai):
        """
            :param: pos - position clicked
            :return: (row, col) - returns the row and col of the position clicked
         """
        if samurai == True:
            if pos[0] < self.width and pos[1] < self.height:
                gap = self.width / 27
                x = pos[0] // gap
                y = pos[1] // gap
                return int(y), int(x)
            else:
                return None
        else:
            if pos[0] < self.width and pos[1] < self.height:
                gap = self.width / 9
                x = pos[0] // gap
                y = pos[1] // gap
                return int(y), int(x)
            else:
                return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def dlx_solve_sudoku(self, size, grid, win):
        """ An efficient Sudoku solver using Algorithm X.

            >>> for solution in solve((3, 3), grid, win):
                    print(*solution, sep='\\n')
            """

        R, C = size
        N = R * C
        X = ([("row and column", rc) for rc in product(range(N), range(N))] +  # row col
             [("row and number", rn) for rn in product(range(N), range(1, N + 1))] +  # row number
             [("column and number", cn) for cn in product(range(N), range(1, N + 1))] +  # col number
             [("number in box in row?", bn) for bn in product(range(N), range(1, N + 1))])  # box number
        Y = dict()
        for r, c, n in product(range(N), range(N), range(1, N + 1)):
            b = (r // R) * R + (c // C)  # box number. // represents floor division
            Y[(r, c, n)] = [
                ("row and column", (r, c)),
                ("row and number", (r, n)),
                ("column and number", (c, n)),
                ("number in box in row?", (b, n))]

        X, Y = self.sudoku_exact_cover(X, Y)
        for i, row in enumerate(grid):  # count of curr iteration (i) and the value at i (row)
            for j, n in enumerate(row):  # curr iteration (j) and value at j (n)
                if n:  # note that 1 == True in python
                    self.sudoku_select(X, Y, (i, j, n))  # X, Y
        for solution in self.solve(X, Y, [], win):
            print("solution type: ", type(solution))
            for (r, c, n) in solution:
                # self.cubes[r][c].temp = n  # test
                # self.place(self.cubes[r][c].temp)  # test
                # self.sketch((int) (n))
                grid[r][c] = n
            yield grid

    def sudoku_exact_cover(self, X, Y):
        X = {j: set() for j in X}
        for i, row in Y.items():
            for j in row:
                X[j].add(i)
        return X, Y

    def solve(self, X, Y, solution, win):
        if not X:
            yield list(solution)
        else:
            c = min(X, key=lambda c: len(X[c]))
            for r in list(X[c]):  # note that r and c are both tuples
                solution.append(r)
                cols = self.sudoku_select(X, Y, r)
                self.sudoku_sketch(r, win)
                for s in self.solve(X, Y, solution, win):
                    yield s
                self.sudoku_deselect(X, Y, r, cols)
                # self.clear(r, cols)  # test
                remove = solution.pop()
                row = remove[0]
                col = remove[1]
                self.select(row, col)
                self.cubes[row][col].temp = 0
                self.sudoku_place(self.cubes[row][col].temp)
                self.sketch(0)
                redraw_window(win, self, 0, 0)
                pygame.display.update()
                # time.sleep(0.05)

    def sudoku_sketch(self, r, win):
        row = r[0]
        col = r[1]
        self.select(row, col)
        self.cubes[row][col].temp = r[2]
        if self.cubes[row][col].temp != 0:
            self.sudoku_place(self.cubes[row][col].temp)
        self.sketch(r[2])
        redraw_window(win, self, 0, 0)
        pygame.display.update()
        time.sleep(0.05)

    def sudoku_select(self, x, y, r):
        cols = []
        for j in y[r]:
            for i in x[j]:
                for k in y[i]:
                    if k != j:
                        x[k].remove(i)
            cols.append(x.pop(j))
        return cols

    def sudoku_deselect(self, x, y, r, cols):
        for j in reversed(y[r]):
            x[j] = cols.pop()
            for i in x[j]:
                for k in y[i]:
                    if k != j:
                        x[k].add(i)

    def sudoku_place(self, val):
        row, col = self.selected
        self.cubes[row][col].set(val)
        self.update_model()

    def sudoku_clear(self, row, col):
        # if self.cubes[row][col].value == 0:
        self.cubes[row][col].set_temp(0)
# End Of Grid Class

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win, samurai):

        fnt = pygame.font.SysFont("comics", 30)
        if not samurai:
            gap = self.width / 9
        else:
            gap = self.width / 27

        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), True, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), True, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected and samurai == False:
            pygame.draw.rect(win, (0, 255, 0), (0, y, gap + self.width, gap), 3)
            pygame.draw.rect(win, (0, 255, 0), (x, 0, gap, self.height), 3)
        if self.selected and samurai == True:
            pygame.draw.rect(win, (0, 255, 0), (0, y, gap + self.width - 140, gap), 3)
            pygame.draw.rect(win, (0, 255, 0), (x, 0, gap, self.height - 120), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


# End Of Grid Class

def redraw_window(win, board, time, strikes, samurai):
    win.fill((255, 255, 255))
    # Draw time
    fnt = pygame.font.SysFont("comics", 20)
    text = fnt.render("Time: " + format_time(time), True, (0, 0, 0))
    win.blit(text, (540 - 200, 750))
    # Draw Strikes
    text = fnt.render(str(strikes), True, (255, 0, 0))
    win.blit(text, (20, 750))

    # code for buttons
    button_top = 550
    button_height = 30
    pygame.draw.rect(win, (216, 191, 216),
                     [120, button_top, 170, button_height])  # (surface, (r, g, b), [left, top, width, height])
    text = fnt.render('New Puzzle', True, (0, 0, 0))
    win.blit(text, (120, button_top))
    pygame.draw.rect(win, (216, 191, 216),
                     [120, button_top + 50, 375, button_height])  # (surface, (r, g, b), [left, top, width, height])
    text = fnt.render('Watch Dancing Links Do It!', True, (0, 0, 0))
    win.blit(text, (120, button_top + 50))
    pygame.draw.rect(win, (216, 191, 216),
                     [120, button_top + 100, 375, button_height])  # (surface, (r, g, b), [left, top, width, height])
    text = fnt.render('Quit', True, (0, 0, 0))
    win.blit(text, (120, button_top + 100))
    pygame.draw.rect(win, (216, 191, 216),
                     [50, button_top + 150, 100, button_height])  # (surface, (r, g, b), [left, top, width, height])
    text = fnt.render('Sudoku - Easy', True, (0, 0, 0))
    win.blit(text, (50, button_top + 150))
    pygame.draw.rect(win, (216, 191, 216),
                     [200, button_top + 150, 100, button_height])  # (surface, (r, g, b), [left, top, width, height])
    text = fnt.render('Sudoku - Medium', True, (0, 0, 0))
    win.blit(text, (200, button_top + 150))

    pygame.draw.rect(win, (216, 191, 216),
                     [350, button_top + 150, 100, button_height])  # (surface, (r, g, b), [left, top, width, height])
    text = fnt.render('Sudoku - Hard', True, (0, 0, 0))
    win.blit(text, (350, button_top + 150))
    pygame.draw.rect(win, (216, 191, 216),
                     [200, 600 + 150, 100, button_height])
    text = fnt.render('Samurai - Sudoku', True, (0, 0, 0))
    win.blit(text, (200, 600 + 150))

    # Draw grid and board

    # board.draw(win)

    board.draw(win, samurai)


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((540, 800))  # (x, y)
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0
    play_time = 0
    samurai = False

    while run:
        if strikes == 3:
            print("3 Mistakes! Board Resetting...")
            board.reset(samurai)
            strikes = 0

        # play_time was encapsulated into this if statement
        # so that when the puzzle is solved the time stops.
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
                        # run = False

            if board.selected and key != None:
                board.sketch(key)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # (x, y) of mouse position
                clicked = board.click(pos, samurai)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
                elif 120 <= pos[0] <= 495 and 550 <= pos[1] <= 580:
                    samurai = False
                    board.new_puzzle(2)
                    board.reset(samurai)
                    strikes = 0
                elif 120 <= pos[0] <= 495 and 600 <= pos[1] <= 630:
                    samurai = False
                    board.reset(samurai)
                    list(board.dlx_solve_sudoku((3, 3), board.board, win))
                elif 120 <= pos[0] <= 495 and 650 <= pos[1] <= 680:
                    pygame.quit()
                elif 50 <= pos[0] <= 150 and 700 <= pos[1] <= 730:
                    samurai = False
                    board.set_puzzle(getPuzzle(1))
                    board.reset(samurai)
                elif 200 <= pos[0] <= 300 and 700 <= pos[1] <= 730:
                    samurai = False
                    board.set_puzzle(getPuzzle(2))
                    board.reset(samurai)
                elif 350 <= pos[0] <= 450 and 700 <= pos[1] <= 730:
                    samurai = False
                    board.set_puzzle(getPuzzle(3))
                    board.reset(samurai)
                elif 200 <= pos[0] <= 300 and 750 <= pos[1] <= 780:
                    samurai = True
                    board.reset(samurai)

        redraw_window(win, board, play_time, strikes, samurai)

        pygame.display.update()


main()
pygame.quit()
