# Capstone
Fall 2021 Capstone Project  

Our Capstone project focuses on solving Sudoku puzzles using the Dancing Link algorithm and visualizing this solving process. Before moving on, I will define some vocabulary that is critical to understanding this project.

- Exact Cover: given S, which is a collection of subsets of X, an exact cover is a subcollection S' of S such that each element in X is contained in exactly one subset of S'.
- Exact Cover Problem: the process of determining whether or not an exact cover exists.
- Algorithm X: an algorithm that finds all solutions to the exact cover problem. Popular exact cover problems include Pentomino tiling, n queens, and ***sudoku***.
- Dancing Link algorithm: an algorithm that allows one to efficiently revert the deletion of a node from a circular doubly-linked list. This makes it a very effective way of implementing backtracking algorithms. It is used to implement Donald Knuth's Algorithm X.



https://github.com/c9victor/Capstone/assets/56898542/0d98dc1d-6805-408f-90bf-89ef4ff9383a



## puzzle_retriever.py
This file retrieves a puzzle of the given difficulty from the csv file. Default difficulty is 2, or medium.

## dlx.py
This file contains our python implementation of the dancing links algorithm. We keep track of a two-dimensional array of nodes, where every row and column of the array is a circular doubly-linked list. Below is a description of critical methods.

### build_constraint_matrix
Used to build the matrix of 1's and 0's which we can use to solve the exact cover problem. We must take into consideration that for a normal 9x9 sudoku puzzle, every position on the board has 4 constraints-
1. row column constraint: every row/column position on the board must have one of the numbers 1-9 populating it.
2. row number constraint: every row must have one and only one of the numbers 1-9.
3. column number constraint: every column must have one and only one of the numbers 1-9.
4. box number constraint: every box must have one and only one of the numbers 1-9.

### create_linked_matrix
The create_linked_matrix function is responsible for creating the linked 2d matrix where every row and column is a circular doubly-linked list. 

### search
Finds every possible solution of the exact cover problem by covering and uncovering nodes to solve the exact cover problem. Note that a proper sudoku puzzle has only *one* solution.

### cover
Covers the column and every row associated with the column.

### uncover
Reverts the cover operation in the exact opposite order that it happened in.

## samuraiGUI.py
Our current version of the GUI.  
Features:
- Users can play a regular game of sudoku
- If the user makes more than 2 mistakes the board resets
- User is timed
- Easy, medium, and hard difficulty levels
- User can press a button to see the dancing links algorithm solve the puzzle

## Future goals
- User can play samurai sudoku
- Get the dancing link algorithm working on samurai puzzles (5 interlinked sudoku puzzle)
