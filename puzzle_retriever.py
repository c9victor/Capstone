import random
import linecache
import numpy as np 


'''
Opens a csv file filled with sudoku puzzles.
The columns of the file are:   x   puzzle   solution   clues   difficulty
The information in the puzzle column is parsed so that we can create a sudoku board.
If the puzzle is not of an acceptable difficulty level then a new one is retrieved.
Note that the first line of the file contains headers; do not attempt to parse it as a puzzle
'''
def get_puzzle(diff=2):  
    # puzzleNum = 1333506  # a very good and hard puzzle
    puzzleNum = random.randint(1, 3000001)  
    #print("Puzzle Number:", puzzleNum) 
    puzzle = linecache.getline("sudoku-3m.csv", puzzleNum)
    puzzle = puzzle.split(',')
    while (not check_diff(puzzle, diff)):
        puzzleNum = random.randint(1, 3000001) 
        #print("Puzzle Number:", puzzleNum) 
        puzzle = linecache.getline("sudoku-3m.csv", puzzleNum)
        puzzle = puzzle.split(',')
    print("Puzzle Number:", puzzleNum) 
    debug(puzzle)
    puzzle = reshape(puzzle)

    return puzzle

'''
Checks the difficulty level of the given puzzle to make sure it is acceptable.
1 = Easy, 2 = Medium, 3 = Hard
'''
def check_diff(puzzle, diff): 
    pdiff = np.double(puzzle[4]) 
    #print("diff", diff, "pdiff", pdiff)
    if diff == 1 and pdiff < 1.5: 
        return True
    elif diff == 2 and pdiff >= 1.5 and pdiff < 3:
        return True 
    elif diff == 3 and pdiff >= 3:
        return True 
    return False

'''
Reshapes the puzzle so that it can be used by the pygame GUI
'''
def reshape(puzzle):
    #print("Puzzle at start:", puzzle[1])  # start board
    #print("Finished puzzle:", puzzle[2])  # finished solution
    reshaped_puzzle = list(puzzle[1].replace('.','0'))
    #print("list():", reshaped_puzzle)
    reshaped_puzzle = [int(numeric_string) for numeric_string in reshaped_puzzle]  # https://www.codegrepper.com/code-examples/python/convert+string+array+to+int+array+python
    #print("string->numeric:", reshaped_puzzle)
    reshaped_puzzle = np.reshape(reshaped_puzzle, (9, 9))
    #print("reshape():\n", reshaped_puzzle)
    return reshaped_puzzle

'''
Used for debugging the program
'''
def debug(puzzle): 
    finish_puzzle = list(puzzle[2])
    finish_puzzle = [int(numeric_string) for numeric_string in finish_puzzle]
    finish_puzzle = np.reshape(finish_puzzle, (9, 9))
    print("finished:\n", finish_puzzle)
