#!/usr/bin/python
from cell import Cell
from board import Board
import boardfromtext

infile = "./game2.csv"

gameboard = boardfromtext.LoadFromFile(infile)
#gameboard = Board()

gameboard.PrintBoardState()

print "Running solver"
if not gameboard.RecursiveSolve():
	print "Failed to solve!"
else:
	print "Solved!"

print gameboard.PrintBoardState()

