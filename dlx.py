import numpy as np

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
    def __init__(self, board=None):
        '''
        need to build a constraint matrix:
        324 columns (4 constraints * 81 positions)
        729 rows (9 possibilities * 81 positions)

        a solved sudoku puzzle has 81 assignments, so
        it will have 81 rows in the DLX solution, each
        filling in 4 of the 324 columns.
        '''
        if board:
            self.test = board 
        else: 
            self.test = [[4, 0, 3, 0, 6, 0, 0, 9, 0],
                         [0, 0, 1, 3, 7, 0, 8, 2, 0],
                         [0, 0, 0, 0, 0, 8, 0, 1, 0], 
                         [5, 0, 0, 0, 0, 0, 3, 4, 6], 
                         [6, 0, 0, 0, 8, 9, 0, 0, 0], 
                         [0, 2, 7, 0, 0, 0, 0, 0, 5], 
                         [8, 0, 0, 7, 3, 4, 2, 0, 0], 
                         [0, 0, 9, 8, 0, 6, 0, 0, 1], 
                         [0, 7, 5, 0, 2, 1, 0, 0, 0]]
        '''
        solution = 
        [[4 8 3 1 6 2 5 9 7]
         [9 6 1 3 7 5 8 2 4]
         [7 5 2 4 9 8 6 1 3]
         [5 9 8 2 1 7 3 4 6]
         [6 3 4 5 8 9 1 7 2]
         [1 2 7 6 4 3 9 8 5]
         [8 1 6 7 3 4 2 5 9]
         [2 4 9 8 5 6 7 3 1]
         [3 7 5 9 2 1 4 6 8]]
        '''
        # self.test = [[1, 0, 0, 1, 0, 0, 1],
        #              [1, 0, 0, 1, 0, 0, 0],
        #              [0, 0, 0, 1, 1, 0, 1],
        #              [0, 0, 1, 0, 1, 1, 0],
        #              [0, 1, 1, 0, 0, 1, 1],
        #              [0, 1, 0, 0, 0, 0, 1]]
        self.head = Node() 
        self.matrix = [[Node() for x in range(20)] for y in range(20)]
        self.numProbRows = 729  # 6
        self.numProbCols = 324  # 7
        self.problem_matrix = [[False for x in range(self.numProbCols)] for y in range(self.numProbRows + 1)]  # need 1 extra for header
        self.solutions = []

        self.build_constraint_matrix(self.test)
        '''
        Initialize the problem matrix based on the given input
        '''
        # for i in range(len(self.problem_matrix)):
        #     for j in range(len(self.problem_matrix[0])):
        #         # set the header column to True
        #         if i == 0:
        #             self.problem_matrix[i][j] = True
        #         elif self.test[i-1][j] == 1:
        #             self.problem_matrix[i][j] = True
    
    def build_constraint_matrix(self, board): 
        rc_constraint = [0] * 81
        rn_constraint = [0] * 81
        cn_constraint = [0] * 81
        bn_constraint = [0] * 81 
        for r in range(len(board)):
            num = 0
            for c in range(len(board[0])):
                if board[r][c] != 0: 
                    rc_constraint[r*9 + c] = 1 
                    rn_constraint[c*9 + num] = 1  # may need to add 1
                    cn_constraint[r*9 + num] = 1  # double-check this one
                    #bn_constraint[something] = 1 
                num += 1
        '''
        flattened = np.array(board).flatten() 
        row = col = counter = 0
        for val in flattened:
            for r in range(len(board)):
                for c in range(len(board[0])):
                    if board[r][c] == val and r == row and c == col:
                        print('val:', val)
                        print('board[r][c]:', str(board[r][c]))
                        print('row:', str(row))
                        print('col:', str(board[r][c]))
                        rc_constraint.append(1)
                    else:
                        rc_constraint.append(0)
            # concatenate the 4 constraints together 
            # and add new row for next position
            counter += 1
            if counter == 9:
                row += 1
                col = 0
            else:
                col += 1
        #print(len(rc_constraint))
        count = 0
        for i in rc_constraint:
            if i == 1:
                count += 1
        print(count)
        '''
        return 0

    '''
    Prints the problem matrix. Useful for debugging
    '''
    def print_problem_matrix(self): 
        for r in self.problem_matrix:
            i = ""
            for c in r:
                i += str(c) + " "
            print(i)

    def getRight(self, index):
        return (index + 1) % self.numProbCols    
    
    def getLeft(self, index):
        return (self.numProbCols - 1) if (index - 1 < 0) else (index - 1)

    def getUp(self, index):
        return (self.numProbRows) if (index - 1 < 0) else (index - 1)  

    def getDown(self, index):
        return (index + 1) % (self.numProbRows + 1)

    '''
    Creates the circular doubly-linked list
    '''
    def createLinkedMatrix(self):
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
                    b = self.getLeft(b)
                    while not self.problem_matrix[a][b] and b != j:
                        b = self.getLeft(b)
                    self.matrix[i][j].left = self.matrix[i][b]

                    # right "pointer"
                    b = j
                    b = self.getRight(b)
                    while not self.problem_matrix[a][b] and b != j:
                        b = self.getRight(b)
                    self.matrix[i][j].right = self.matrix[i][b]

                    # up "pointer"
                    b = j
                    a = self.getUp(a)
                    while not self.problem_matrix[a][b] and a != i:
                        a = self.getUp(a)
                    self.matrix[i][j].up = self.matrix[a][j]

                    # down "pointer"
                    a = i
                    a = self.getDown(a)
                    while not self.problem_matrix[a][b] and a != i:
                        a = self.getDown(a) 
                    self.matrix[i][j].down = self.matrix[a][j]
        #link header right pointer to col header of the 1st col
        self.head.right = self.matrix[0][0]

        #link header left pointer to col header of the last col
        self.head.left = self.matrix[0][self.numProbCols - 1]

        self.matrix[0][0].left = self.head
        self.matrix[0][self.numProbCols - 1].right = self.head
        return self.head
    
    def cover(self, target): 
        #get the pointer to the col header
        #to which this node belongs 
        colNode = target.column 

        #unlink column header from it's neighbors
        colNode.left.right = colNode.right
        colNode.right.left = colNode.left

        #Move down the column and remove each row by traversing right
        row = colNode.down
        while row != colNode:
            rightNode = row.right 
            while rightNode != row:
                rightNode.up.down = rightNode.down
                rightNode.down.up = rightNode.up
    
                #after unlinking row node, decrement the
                #node count in column header
                self.matrix[0][rightNode.colID].num -= 1

                #traverse
                rightNode = rightNode.right 
            row = row.down 
    
    def uncover(self, target):
        # get the pointer to the header of column
        # to which this node belong  
        colNode = target.column
    
        # Move down the column and link back
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

    '''
    Get the column with the smallest amount of ones
    '''
    def getMinColumn(self): 
        h = self.head
        min_col = h.right
        h = h.right.right
        
        if h.num < min_col.num:
            min_col = h
        h = h.right
        while h != self.head:
            if h.num < min_col.num:
                min_col =h
            h = h.right
    
        return min_col
    
    def printSolutions(self):
        solution = ""
        for i in self.solutions:
            solution += str(i.rowID) + " "
        print('Printing Solutions:', solution) 
    
    # searches for all exact cover solutions
    def search(self, num): 
        # if no column left, then we must
        # have found the solution
        if(self.head.right == self.head):
            self.printSolutions()
            return
        
        #deterministically choose the smallest col
        column = self.getMinColumn() 
        #cover chosen col 
        self.cover(column)
        
        rowNode = column.down
        while rowNode != column:
            rightNode = rowNode.right
            self.solutions.append(rowNode) # push()
            while rightNode != rowNode:
                self.cover(rightNode)
                rightNode = rightNode.right

            #recursively move to level k+1
            self.search(num+1)

            # if solution in not possible, backtrack (uncover)
            # and remove the selected row (set) from solution
            self.solutions.pop() 
            
            column = rowNode.column
            leftNode = rowNode.left
            while leftNode != rowNode:
                self.uncover(leftNode)
                leftNode = leftNode.left

            rowNode = rowNode.down
        self.uncover(column)


dlx = DLX() 
# dlx.createLinkedMatrix()
# dlx.search(0)
