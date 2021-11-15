# Capstone
Fall 2021 Capstone Project  

Our Capstone project focuses on solving Sudoku puzzles using the Dancing Link algorithm and visualizing this solving process. Before moving on, I will define some vocabulary that is critical to understanding this project.

- Exact Cover: given S, which is a collection of subsets of X, an exact cover is a subcollection S' of S such that each element in X is contained in exactly one subset of S'.
- Exact Cover Problem: the process of determining whether or not an exact cover exists.
- Algorithm X: an algorithm that finds all solutions to the exact cover problem. Popular exact cover problems include Pentomino tiling, n queens, and ***sudoku***.
- Dancing Link algorithm: an algorithm that allows one to efficiently revert the deletion of a node from a circular doubly-linked list. This makes it a very effective way of implementing backtracking algorithms. It is used to implement Donald Knuth's Algorithm X.

## puzzle_retriever.py
This file retrieves a puzzle of the given difficulty from the csv file

## dlx.py
This file 
