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
    def __init__(self): 
        self.test = [[1, 0, 0, 1, 0, 0, 1],
                     [1, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 1, 1, 0, 1],
                     [0, 0, 1, 0, 1, 1, 0],
                     [0, 1, 1, 0, 0, 1, 1],
                     [0, 1, 0, 0, 0, 0, 1]]
        self.head = Node() 
        self.matrix = [[Node() for x in range(20)] for y in range(20)]
        self.numProbRows = 6
        self.numProbCols = 7
        self.problem_matrix = [[False for x in range(self.numProbCols)] for y in range(self.numProbRows + 1)]  # need 1 extra for header
        self.solutions = []

        '''
        Initialize the problem matrix based on the given input
        '''
        for i in range(len(self.problem_matrix)):
            for j in range(len(self.problem_matrix[0])):
                # set the header column to True
                if i == 0:
                    self.problem_matrix[i][j] = True
                elif self.test[i-1][j] == 1:
                    self.problem_matrix[i][j] = True
    
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
        rightNode = row.right  
        while row != colNode:
            print('1')  # infinite looping in 2nd while loop
            while rightNode != row: 
                if rightNode is row:
                    print('oh')
                rightNode.up.down = rightNode.down
                rightNode.down.up = rightNode.up
    
                #after unlinking row node, decrement the
                #node count in column header
                self.matrix[0][rightNode.colID].num -= 1

                #traverse
                rightNode = rightNode.right 
            row = row.down
    
    def uncover(self, target):# get the pointer to the header of column
        # to which this node belong  
        colNode = target.column
    
        # Move down the column and link back
        # each row by traversing left

        rowNode = colNode.up
        leftNode = rowNode.left
        #C version below
        #for(rowNode = colNode.up; rowNode != colNode; rowNode = rowNode.up) 
        #    for(leftNode = rowNode.left; leftNode != rowNode; leftNode = leftNode.left) 
        while rowNode != colNode:
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

    def getMinColumn(self): 
        h = self.head
        min_col = h.right
        h = h.right.right
        # if(h->num < min_col->num)
        # {
        #     min_col = h;
        # }
        # h = h->right;
        if h.num < min_col.num:
            min_col = h
        h = h.right
        while h != self.head:
            if h.num < min_col.num:
                min_col =h
            h = h.right
    
        return min_col
    
    def printSolutions(self):
        print('Printing Solutions: ')
        for i in self.solutions:
            print(i)
    
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
        rightNode = rowNode.right
        while rowNode != column:
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
dlx.createLinkedMatrix()
dlx.search(0)
