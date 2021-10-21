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
                     [0, 1, 0, 0, 0, 0, 1],
                     [1, 0, 1, 1, 0, 0, 0]]
        self.head = Node() 
        self.matrix = [[Node() for x in range(7)] for y in range(7)]
        self.numProbRows = 8
        self.numProbCols = 7
        self.problem_matrix = [[False for x in range(self.numProbCols)] for y in range(self.numProbRows)]
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
        return self.numProbRows if (index - 1 < 0) else (index - 1)

    def getDown(self, index):
        return (index + 1) % (self.numProbRows + 1)

    def createLinkedMatrix(self):
        for i in self.numProbRows + 1:
            for j in self.numProbCols:
                if self.problem_matrix[i][j]:
                    '''
                    if i is 1 and it's not a part of the column header
                    increment node count of column header
                    '''
                    if i:
                        self.matrix[0][j] += 1
                    
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
                    


dlx = DLX() 
dlx.print_problem_matrix()