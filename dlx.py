# import puzzle_retriever  # for testing purposes

class Node:
    def __init__(self, num=0): 
        self.num = num
        self.rowID = None
        self.colID = None
        self.right = None 
        self.left = None 
        self.up = None
        self.down = None
        self.column = None

class DLX:
    def __init__(self, board=None, samurai=False):
        '''
        need to build a constraint matrix:
        324 columns (4 constraints * 81 positions)
        729 rows (9 possibilities * 81 positions)

        a solved sudoku puzzle has 81 assignments, so
        it will have 81 rows in the DLX solution, each
        filling in 4 of the 324 columns.
        '''
        # self.board = puzzle_retriever.get_puzzle()  # for testing purposes
        self.board = board
        self.head = Node()
        if samurai:
            self.numProbRows = 3969
            self.numProbCols = 8820
            self.numPositions = 441
        else:
            self.numProbRows = 729
            self.numProbCols = 324
            self.numPositions = 81
        print('starting initialization process')
        self.matrix = [[Node() for x in range(self.numProbCols)] for y in range(self.numProbRows + 1)]  # matrix of LL's used by the DLX algo
        print('made matrix')
        self.problem_matrix = [[False for x in range(self.numProbCols)] for y in range(self.numProbRows + 1)]  # need 1 extra for header
        print('made problem matrix')
        self.constraint_matrix = self.build_constraint_matrix(self.board, samurai)  # constraint matrix of 1's and 0's is used to build problem matrix
        self.solutions = [] 
        self.final_solutions = [] 
        self.all_covers_uncovers = []  # list of all nodes that were covered/uncovered in order
        self.cover_or_uncover = []  # corresponds to above list. 1 = covered, 0 = uncovered

        '''
        Initialize the problem matrix based on the given input
        '''
        for i in range(len(self.problem_matrix)):
            for j in range(len(self.problem_matrix[0])):
                # set the header column to True
                if i == 0:
                    self.problem_matrix[i][j] = True
                elif self.constraint_matrix[i-1][j] == 1:
                    self.problem_matrix[i][j] = True
    
    def build_constraint_matrix(self, board, samurai):
        constraint_matrix = [[0] * self.numProbCols] * self.numProbRows
        print('initialized constraint matrix')
        # numPositions = 81
        num_iters = 0
        for r in range(len(board)):
            for c in range(len(board[0])):        
                for num in range(1, 10):  # iterates through 1-9
                    if samurai:
                        tl_rc_constraint = [0] * self.numPositions  # top left row col constraint
                        tl_rn_constraint = [0] * self.numPositions  # top left row number constraint
                        tl_cn_constraint = [0] * self.numPositions  # top left col number constraint
                        tl_bn_constraint = [0] * self.numPositions  # top left box number constraint

                        tr_rc_constraint = [0] * self.numPositions  # top right row col constraint
                        tr_rn_constraint = [0] * self.numPositions  # top right row number constraint
                        tr_cn_constraint = [0] * self.numPositions  # top right col number constraint
                        tr_bn_constraint = [0] * self.numPositions  # top right box number constraint

                        bl_rc_constraint = [0] * self.numPositions  # bottom left row col constraint
                        bl_rn_constraint = [0] * self.numPositions  # bottom left row number constraint
                        bl_cn_constraint = [0] * self.numPositions  # bottom left col number constraint
                        bl_bn_constraint = [0] * self.numPositions  # bottom left box number constraint

                        br_rc_constraint = [0] * self.numPositions  # bottom right row col constraint
                        br_rn_constraint = [0] * self.numPositions  # bottom right row number constraint
                        br_cn_constraint = [0] * self.numPositions  # bottom right col number constraint
                        br_bn_constraint = [0] * self.numPositions  # bottom right box number constraint

                        c_rc_constraint = [0] * self.numPositions  # center row col constraint
                        c_rn_constraint = [0] * self.numPositions  # center row number constraint
                        c_cn_constraint = [0] * self.numPositions  # center col number constraint
                        c_bn_constraint = [0] * self.numPositions  # center box number constraint
                        if (board[r][c] != 0 and board[r][c] == num) or board[r][c] == 0: 
                            # horizontal spaces that are not actually part of the board
                            if 9 <= r <= 11 and (0 <= c <= 5 or 15 <= c <= 20):
                                continue
                            # vertical spaces that are not actually part of the board
                            elif 9 <= c <= 11 and (0 <= r <= 5 or 15 <= r <= 20):
                                continue
                            # top left puzzle positions
                            if r <= 8 and c <= 8:
                                tl_rc_constraint[r*9 + c] = 1 
                                tl_rn_constraint[c*9 + num - 1] = 1
                                tl_cn_constraint[r*9 + num - 1] = 1
                                tl_bn_constraint[((r // 3) * 3 + (c // 3)) * 9 + num - 1] = 1  # b * 9 + (num - 1) 
                            # top right puzzle positions --> NOT DONE YET
                            if r <= 8 and c >= 12:
                                tr_rc_constraint[r*21 + c] = 1
                                tr_rn_constraint[c*21 + num - 1] = 1
                                tr_cn_constraint[r*9 + num - 1] = 1
                                tr_bn_constraint[0] = 1
                            # bottom left puzzle positions --> NOT DONE YET
                            if r >= 12 and c <= 8:
                                bl_rc_constraint[0] = 1
                                bl_rn_constraint[0] = 1
                                bl_cn_constraint[0] = 1
                                bl_bn_constraint[0] = 1
                            # bottom right puzzle positions --> NOT DONE YET
                            if r >= 12 and c >= 12:
                                br_rc_constraint[0] = 1
                                br_rn_constraint[0] = 1
                                br_cn_constraint[0] = 1
                                br_bn_constraint[0] = 1
                            # center puzzle positions --> NOT DONE YET
                            if 6 <= r <= 14 and 6 <= c <= 14:
                                c_rc_constraint[0] = 1
                                c_rn_constraint[0] = 1
                                c_cn_constraint[0] = 1
                                c_bn_constraint[0] = 1
                            
                            constraint_matrix[num_iters] = tl_rc_constraint + tl_rn_constraint + tl_cn_constraint + tl_bn_constraint
                            + tr_rc_constraint + tr_rn_constraint + tr_cn_constraint + tr_bn_constraint
                            + bl_rc_constraint + bl_rn_constraint + bl_cn_constraint + bl_bn_constraint
                            + br_rc_constraint + br_rn_constraint + br_cn_constraint + br_bn_constraint
                            + c_rc_constraint + c_rn_constraint + c_cn_constraint + c_bn_constraint
                    else:
                        # want to reset the constraints for every 81 positions on the board every iteration
                        rc_constraint = [0] * self.numPositions  # row col constraint
                        rn_constraint = [0] * self.numPositions  # row number constraint
                        cn_constraint = [0] * self.numPositions  # col number constraint
                        bn_constraint = [0] * self.numPositions  # box number constraint
                        '''
                        For squares that are already filled, you generate the one row that describes that assignment.
                        Else, generate the possibility that it is each number, one thru 9

                        if spquare is filled -> generate row with given number
                        else if square is empty -> generate every possibility for row
                        '''
                        if (board[r][c] != 0 and board[r][c] == num) or board[r][c] == 0: 
                            rc_constraint[r*9 + c] = 1 
                            rn_constraint[c*9 + num - 1] = 1
                            cn_constraint[r*9 + num - 1] = 1
                            # // represents floor division
                            bn_constraint[((r // 3) * 3 + (c // 3)) * 9 + num - 1] = 1  # b * 9 + (num - 1) 
                            # concatenate constraints together
                            constraint_matrix[num_iters] = rc_constraint + rn_constraint + cn_constraint + bn_constraint  
                    num_iters += 1
        
        return constraint_matrix

    def map_solved_to_board(self):
        '''
        for row in solutions:
            grab row/col from 1st constraint
            grab number out of 2nd constraint
        '''
        for solution in self.solutions: 
            self.final_solutions.append(solution)
            s_row = solution.rowID
            first = self.constraint_matrix[s_row-1].index(1)
            second = self.constraint_matrix[s_row-1].index(1, 81)  # find:1  start_at:81 
            row = int(first / 9) 
            col = first % 9 
            num = int((second - 80) % 9)
            # w/out this if, c0 would have a 9 but c1-c8 would have 0's instead of 9's
            if num == 0:
                num = 9
            self.board[row][col] = num 
        print("solution:")
        for i in range(len(self.board)):
            print(self.board[i])
        return

    '''
    Prints the problem matrix. Useful for debugging
    '''
    def print_problem_matrix(self): 
        for r in self.problem_matrix:
            i = ""
            for c in r:
                i += str(c) + " "
            print(i)

    def get_right(self, index):
        return (index + 1) % self.numProbCols    
    
    def get_left(self, index):
        return (self.numProbCols - 1) if (index - 1 < 0) else (index - 1)

    def get_up(self, index):
        return (self.numProbRows) if (index - 1 < 0) else (index - 1)  

    def get_down(self, index):
        return (index + 1) % (self.numProbRows + 1)

    '''
    Creates the circular doubly-linked list
    '''
    def create_linked_matrix(self):
        for i in range(self.numProbRows + 1):
            for j in range(self.numProbCols):
                if self.problem_matrix[i][j]:
                    '''
                    if i is 1 and it's not a part of the column header
                    increment node count of column header
                    '''
                    if i:
                        self.matrix[0][j].num += 1
                    
                    # add "pointer" to column header
                    self.matrix[i][j].column = self.matrix[0][j]
                    # set row and col ID
                    self.matrix[i][j].rowID = i
                    self.matrix[i][j].colID = j

                    # link node to neighbors
                    a = i
                    b = j

                    # left "pointer"
                    b = self.get_left(b)
                    while not self.problem_matrix[a][b] and b != j:
                        b = self.get_left(b)
                    self.matrix[i][j].left = self.matrix[i][b]

                    # right "pointer"
                    b = j
                    b = self.get_right(b)
                    while not self.problem_matrix[a][b] and b != j:
                        b = self.get_right(b)
                    self.matrix[i][j].right = self.matrix[i][b]

                    # up "pointer"
                    b = j
                    a = self.get_up(a)
                    while not self.problem_matrix[a][b] and a != i:
                        a = self.get_up(a) 
                    self.matrix[i][j].up = self.matrix[a][j]

                    # down "pointer"
                    a = i
                    a = self.get_down(a)
                    while not self.problem_matrix[a][b] and a != i:
                        a = self.get_down(a) 
                    self.matrix[i][j].down = self.matrix[a][j]
        #link header right pointer to col header of the 1st col
        self.head.right = self.matrix[0][0]

        #link header left pointer to col header of the last col
        self.head.left = self.matrix[0][self.numProbCols - 1]

        self.matrix[0][0].left = self.head
        self.matrix[0][self.numProbCols - 1].right = self.head
        return self.head
    
    def cover(self, target): 
        # get the pointer to the col header
        # to which this node belongs 
        colNode = target.column 

        # unlink column header from it's neighbors
        colNode.left.right = colNode.right
        colNode.right.left = colNode.left

        # move down the column and remove each row by traversing right
        row = colNode.down
        # self.place(row)  # EXPERIMENTAL
        while row != colNode:
            rightNode = row.right 
            while rightNode != row:
                rightNode.up.down = rightNode.down
                rightNode.down.up = rightNode.up
    
                # after unlinking row node, decrement the
                # node count in column header
                self.matrix[0][rightNode.colID].num -= 1

                # traverse
                rightNode = rightNode.right 
            row = row.down 
    
    def uncover(self, target):
        # get the pointer to the header of column
        # to which this node belong  
        colNode = target.column
    
        # move down the column and link back
        # each row by traversing left
        rowNode = colNode.up 
        while rowNode != colNode:
            leftNode = rowNode.left
            while leftNode != rowNode:
                leftNode.up.down = leftNode
                leftNode.down.up = leftNode
    
                # after linking row node, increment the
                # node count in column header
                self.matrix[0][leftNode.colID].num += 1

                leftNode = leftNode.left
            rowNode = rowNode.up
    
        # link the column header from it's neighbors
        colNode.left.right = colNode
        colNode.right.left = colNode

    # Get the column with the smallest amount of ones
    def get_min_column(self): 
        h = self.head
        min_col = h.right
        h = h.right.right
        
        if h.num < min_col.num:
            min_col = h
        h = h.right
        while h != self.head:
            if h.num < min_col.num:
                min_col = h
            h = h.right
    
        return min_col
    
    def print_solutions(self):
        solution = ""  
        for i in self.solutions:
            solution += str(i.rowID) + " "
        print('Printing Solutions:', solution)
    
    # searches for all exact cover solutions
    def search(self, num):  
        # if no column left, then we must
        # have found the solution
        if(self.head.right == self.head):
            #self.print_solutions()
            #self.map_solved_to_board()
            return

        # deterministically choose the smallest col
        column = self.get_min_column() 

        # cover chosen col 
        self.cover(column)
        
        rowNode = column.down 
        
        while rowNode != column: 
            self.solutions.append(rowNode)  # push() 
            self.all_covers_uncovers.append(rowNode)
            self.cover_or_uncover.append(1)
            
            rightNode = rowNode.right
            while rightNode != rowNode:
                self.cover(rightNode)
                rightNode = rightNode.right

            # recursively move to level k+1
            self.search(num+1)
            
            # if solution is not possible, backtrack (uncover)
            # and remove the selected row (set) from solution
            x = self.solutions.pop()  
            self.all_covers_uncovers.append(x)
            self.cover_or_uncover.append(0)

            column = rowNode.column
            leftNode = rowNode.left
            while leftNode != rowNode:
                self.uncover(leftNode)
                leftNode = leftNode.left

            rowNode = rowNode.down
        self.uncover(column)


# dlx = DLX()  
# dlx.create_linked_matrix() 
# dlx.search(0) 
