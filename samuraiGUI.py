# samuraiGUI.py - RUN THIS FILE
import puzzle_retriever  # our file
from puzzle_retriever import get_puzzle
import dlx  # our file
import pygame
from solver import solve, valid
import time
pygame.font.init()


class Grid:
    board = get_puzzle(1)

    samurai_board = [[0, 5, 1, 0, 6, 7, 2, 0, 8, 0, 0, 0, 9, 0, 8, 5, 6, 0, 7, 2, 0],
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

    samurai_correct = [[9, 5, 1, 4, 6, 7, 2, 3, 8, 0, 0, 0, 9, 1, 8, 5, 6, 3, 7, 2, 4],
                      [8, 7, 4, 1, 3, 2, 9, 6, 5, 0, 0, 0, 4, 2, 7, 9, 1, 8, 6, 5, 3],
                      [6, 3, 2, 5, 9, 8, 7, 1, 4, 0, 0, 0, 3, 5, 6, 4, 7, 2, 8, 9, 1],
                      [4, 1, 8, 2, 7, 6, 5, 9, 3, 0, 0, 0, 7, 9, 1, 3, 5, 4, 2, 8, 6],
                      [5, 2, 7, 9, 1, 3, 8, 4, 6, 0, 0, 0, 8, 3, 5, 2, 9, 6, 4, 1, 7],
                      [3, 6, 9, 8, 4, 5, 1, 7, 2, 0, 0, 0, 2, 6, 4, 7, 8, 1, 5, 3, 9],
                      [1, 8, 3, 6, 5, 9, 4, 2, 7, 3, 5, 1, 6, 8, 9, 1, 4, 5, 3, 7, 2],
                      [2, 4, 6, 7, 8, 1, 3, 5, 9, 8, 6, 7, 1, 4, 2, 8, 3, 7, 9, 6, 5],
                      [7, 9, 5, 3, 2, 4, 6, 8, 1, 9, 2, 4, 5, 7, 3, 6, 2, 9, 1, 4, 8],
                      [0, 0, 0, 0, 0, 0, 7, 9, 5, 4, 3, 8, 2, 1, 5, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 8, 1, 5, 2, 7, 6, 3, 9, 4, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 2, 3, 4, 5, 1, 9, 7, 6, 8, 0, 0, 0, 0, 0, 0],
                      [9, 1, 6, 3, 4, 2, 5, 7, 8, 6, 4, 3, 9, 2, 1, 6, 3, 5, 7, 4, 8],
                      [4, 3, 7, 5, 1, 8, 9, 6, 2, 1, 8, 5, 4, 3, 7, 8, 1, 9, 6, 2, 5],
                      [8, 5, 2, 6, 9, 7, 1, 4, 3, 7, 9, 2, 8, 5, 6, 2, 7, 4, 3, 9, 1],
                      [3, 8, 5, 2, 7, 6, 4, 9, 1, 0, 0, 0, 6, 7, 5, 4, 8, 2, 1, 3, 9],
                      [6, 9, 1, 8, 3, 4, 2, 5, 7, 0, 0, 0, 3, 1, 4, 9, 6, 7, 5, 8, 2],
                      [2, 7, 4, 9, 5, 1, 8, 3, 6, 0, 0, 0, 2, 9, 8, 3, 5, 1, 4, 6, 7],
                      [1, 6, 9, 7, 8, 5, 3, 2, 4, 0, 0, 0, 5, 6, 3, 7, 9, 8, 2, 1, 4],
                      [7, 4, 3, 1, 2, 9, 6, 8, 5, 0, 0, 0, 1, 4, 9, 5, 2, 6, 8, 7, 3],
                      [5, 2, 8, 4, 6, 3, 7, 1, 9, 0, 0, 0, 7, 8, 2, 1, 4, 3, 9, 5, 6]]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def new_puzzle(self, diff):
        self.board = get_puzzle(diff)

    def reset(self, samurai):
        if samurai:
            self.board = self.samurai_board
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

    def draw(self, win, samurai, color):
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
                    self.cubes[i][j].draw(win, samurai, color)

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
                    self.cubes[i][j].draw(win, samurai, color)

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

    def dlx_place(self, val):
        row, col = self.selected
        self.cubes[row][col].set(val)
        self.update_model()
    
    def dlx_sketch(self, r, c, n, win, color=None, strikes=0):
        self.select(r, c)
        self.cubes[r][c].temp = n    
        self.dlx_place(self.cubes[r][c].temp)
        self.sketch(n)
        redraw_window(win, self, 0, strikes, False, color) 
        pygame.display.update()  
        time.sleep(0.07)  

    def dlx_show(self, dlx, win):  
        allMoves = dlx.all_covers_uncovers
        covered = dlx.cover_or_uncover
        numMoves = int(len(allMoves) / 2)
        print('num moves:', numMoves)  # divided by 2 because every cover gets uncovered
        strikes = 0
        for move in range(len(allMoves)):
            s_row = allMoves[move].rowID
            first = dlx.constraint_matrix[s_row-1].index(1)
            second = dlx.constraint_matrix[s_row-1].index(1, 81)  # find:1  start_at:81 
            row = int(first / 9) 
            col = first % 9  
            num = (second - 80) % 9 
            # w/out this if, c0 would have a 9 but c1-c8 would have 0's instead of 9's
            if num == 0:
                num = 9
            
            # we don't want to sketch over the starting clues
            if self.board[row][col] != 0: 
                continue
            elif covered[move]:
                self.dlx_sketch(row, col, num, win, (66, 173, 245), strikes)  # (r, g, b)
            elif move: 
                strikes += 1
                # dlx_show -> dlx_sketch -> redraw_window -> board.draw -> cubes.draw 
                self.dlx_sketch(row, col, 0, win, (245, 66, 173), strikes)  # (r, g, b)
                # increment mistakes count
                #def redraw_window(win, board, time, strikes, samurai, color=None):

            
            if self.is_finished():
                return 
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

    def draw(self, win, samurai, color=None): 
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

        # Draw lines when selecting a box
        if self.selected and samurai == False:
            pygame.draw.rect(win, color, (0, y, gap + self.width, gap), 3)
            pygame.draw.rect(win, color, (x, 0, gap, self.height), 3)
        # if self.selected and samurai == True:
        #     pygame.draw.rect(win, color, (0, y, gap + self.width - 140, gap), 3)
        #     pygame.draw.rect(win, color, (x, 0, gap, self.height - 120), 3)

        # NEW STUFF FOR SAM SUDOKU
        if self.selected and samurai == True:
            gap = self.width / 27
            # Options for center box
            if 6 <= self.row <= 14 and 6 <= self.col <= 14:
                if 9 <= self.col <= 11:
                    # Center box, normal size highlight
                    if 9 <= self.row <= 11:
                        pygame.draw.rect(win, color, (120, y, gap + self.width - 380, gap), 3)
                        pygame.draw.rect(win, color, (x, 120, gap, self.height - 355), 3)

                    # Top three rows of center box or bottom three rows, long highlighting size
                    if 12 <= self.row <= 14 or 6 <= self.row <= 8:
                        #pygame.draw.rect(win, color, (0, y, gap + self.width - 125, gap), 3)
                        pygame.draw.rect(win, color, (0, y, gap + self.width - 135, gap), 3)
                        pygame.draw.rect(win, color, (x, 120, gap, self.height - 355), 3)
                elif 9 <= self.row <= 11 and (6 <= self.col <= 9 or 12 <= self.col <= 14):
                    pygame.draw.rect(win, color, (120, y, gap + self.width - 380, gap), 3)
                    pygame.draw.rect(win, color, (x, 0, gap, self.height - 120), 3)
                else:
                    #pygame.draw.rect(win, color, (120, y, gap + self.width - 380, gap), 3)
                    pygame.draw.rect(win, color, (0, y, gap + self.width - 140, gap), 3) 
                    pygame.draw.rect(win, color, (x, 0, gap, self.height - 120), 3)


            # Top left corner box, normal size highlight
            if 0 <= self.row <= 5 and 0 <= self.col <= 5:
                pygame.draw.rect(win, color, (0, y, gap + self.width - 380, gap), 3)
                pygame.draw.rect(win, color, (x, 0, gap, self.height - 355), 3)

            # Top left corner, long highlight size
            if 6 <= self.col <= 8 and 0 <= self.row <= 5:
                pygame.draw.rect(win, color, (0, y, gap + self.width - 380, gap), 3)
                pygame.draw.rect(win, color, (x, 0, gap, self.height - 120), 3)

            # Top left corner, annoying crap
            if 0 <= self.col <= 5 and 6 <= self.row <= 8:
                pygame.draw.rect(win, color, (0, y, gap + self.width - 140, gap), 3)
                pygame.draw.rect(win, color, (x, 0, gap, self.height - 360), 3)

            # Bottom left corner box, normal size highlight
            if 15 <= self.row <= 20 and 0 <= self.col <= 5:
                pygame.draw.rect(win, color, (0, y, gap + self.width - 380, gap), 3)
                pygame.draw.rect(win, color, (x, 240, gap, self.height - 355), 3)

            # Bottom left corner box, long highlighting
            if 6 <= self.col <= 8 and 15 <= self.row <= 20:
                pygame.draw.rect(win, color, (0, y, gap + self.width - 380, gap), 3)
                pygame.draw.rect(win, color, (x, 0, gap, self.height - 120), 3)

            # Bottom left corner box, annoying corner
            if 12 <= self.row <= 14 and 0 <= self.col <= 5:
                pygame.draw.rect(win, color, (0, y, gap + self.width - 140, gap), 3)
                pygame.draw.rect(win, color, (x, 240, gap, self.height - 360), 3)

            # Top right corner box, normal size highlight
            if 0 <= self.row <= 5 and 15 <= self.col <= 20:
                pygame.draw.rect(win, color, (240, y, gap + self.width - 380, gap), 3)
                pygame.draw.rect(win, color, (x, 0, gap, self.height - 360), 3)

            # Top right corner box, long highlighting size
            if 12 <= self.col <= 14 and 0 <= self.row <= 5:
                pygame.draw.rect(win, color, (240, y, gap + self.width - 380, gap), 3)
                pygame.draw.rect(win, color, (x, 0, gap, self.height - 120), 3)

            # Top right corner box, annoying crap
            if 6 <= self.row <= 8 and 15 <= self.col <= 20:
                pygame.draw.rect(win, color, (0, y, gap + self.width - 140, gap), 3)
                pygame.draw.rect(win, color, (x, 0, gap, self.height - 360), 3)

            # Bottom right corner box, normal size highlight
            if 15 <= self.row <= 20 and 15 <= self.col <= 20:
                pygame.draw.rect(win, color, (240, y, gap + self.width - 380, gap), 3)
                pygame.draw.rect(win, color, (x, 240, gap, self.height - 360), 3)

            # Bottom right corner box, long highlighting size
            if 15 <= self.row <= 20 and 12 <= self.col <= 14:
                pygame.draw.rect(win, color, (240, y, gap + self.width - 380, gap), 3)
                pygame.draw.rect(win, color, (x, 0, gap, self.height - 120), 3)

            # Bottom right corner box, annoying crap
            if 12 <= self.row <= 14 and 15 <= self.col <= 20:
                pygame.draw.rect(win, color, (0, y, gap + self.width - 140, gap), 3)
                pygame.draw.rect(win, color, (x, 240, gap, self.height - 360), 3)
        # END NEW STUFF FOR SAM SUDOKU

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


# End Of Grid Class

def redraw_window(win, board, time, strikes, samurai, color=None):
    win.fill((255, 255, 255))
    # Draw time
    fnt = pygame.font.SysFont("comics", 20)
    text = fnt.render("Time: " + format_time(time), True, (0, 0, 0))
    win.blit(text, (540 - 200, 750))
    # Draw Strikes
    text = fnt.render(str(strikes), True, (255, 0, 0))
    win.blit(text, (20, 750))

    # Code for buttons
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
                     [200, button_top + 150, 120, button_height])  # (surface, (r, g, b), [left, top, width, height])
    text = fnt.render('Sudoku - Medium', True, (0, 0, 0))
    win.blit(text, (200, button_top + 150))

    pygame.draw.rect(win, (216, 191, 216),
                     [350, button_top + 150, 100, button_height])  # (surface, (r, g, b), [left, top, width, height])
    text = fnt.render('Sudoku - Hard', True, (0, 0, 0))
    win.blit(text, (350, button_top + 150))
    pygame.draw.rect(win, (216, 191, 216),
                     [200, 600 + 150, 120, button_height])
    text = fnt.render('Samurai - Sudoku', True, (0, 0, 0))
    win.blit(text, (200, 600 + 150))

    # Draw grid and board
    board.draw(win, samurai, color)


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

            if board.selected and key != None:
                board.sketch(key)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # (x, y) of mouse position
                clicked = board.click(pos, samurai)
                # clicked a position on the board
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
                # new puzzle button (with default difficulty)
                elif 120 <= pos[0] <= 495 and 550 <= pos[1] <= 580:
                    samurai = False
                    board.new_puzzle(2)
                    board.reset(samurai)
                    strikes = 0
                # dancing links button clicked
                elif 120 <= pos[0] <= 495 and 600 <= pos[1] <= 630:
                    # samurai = False
                    board.reset(samurai) 
                    dancing_links = dlx.DLX(board.board, samurai)
                    dancing_links.create_linked_matrix()
                    dancing_links.search(0)
                    board.dlx_show(dancing_links, win)
                # quit button hit
                elif 120 <= pos[0] <= 495 and 650 <= pos[1] <= 680:
                    pygame.quit()
                # generate an easy puzzle
                elif 50 <= pos[0] <= 150 and 700 <= pos[1] <= 730:
                    samurai = False
                    board.set_puzzle(get_puzzle(1))
                    board.reset(samurai)
                # generate a medium puzzle
                elif 200 <= pos[0] <= 320 and 700 <= pos[1] <= 730:
                    samurai = False
                    board.set_puzzle(get_puzzle(2))
                    board.reset(samurai)
                # generate a hard puzzle
                elif 350 <= pos[0] <= 450 and 700 <= pos[1] <= 730:
                    samurai = False
                    board.set_puzzle(get_puzzle(3))
                    board.reset(samurai)
                # generate a samurai puzzle
                elif 200 <= pos[0] <= 320 and 750 <= pos[1] <= 780:
                    samurai = True
                    board.reset(samurai)

        redraw_window(win, board, play_time, strikes, samurai, (66, 173, 245))
        pygame.display.update()


main()
pygame.quit()
