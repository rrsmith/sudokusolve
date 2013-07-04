#!/usr/bin/python
from cell import Cell
from board import Board

gameboard = Board()

#for row in gameboard.rowset:
#	for y in row:
#		print "%s" %  y

#print "Do the things."

gameboard.SetCellValue(0, 0, 2)
gameboard.SetCellValue(0, 1, 1)
gameboard.SetCellValue(0, 2, 5)
gameboard.SetCellValue(2, 0, 6)
gameboard.SetCellValue(2, 2, 9)

gameboard.SetCellValue(1, 4, 8)
gameboard.SetCellValue(2, 5, 5)

gameboard.SetCellValue(0, 8, 8)
gameboard.SetCellValue(1, 7, 1)

gameboard.SetCellValue(3, 2, 6)
gameboard.SetCellValue(5, 0, 8)

gameboard.SetCellValue(4, 3, 6)
gameboard.SetCellValue(4, 4, 4)
gameboard.SetCellValue(4, 5, 9)

gameboard.SetCellValue(3, 8, 3)
gameboard.SetCellValue(5, 6, 6)

gameboard.SetCellValue(7, 1, 6)
gameboard.SetCellValue(8, 0, 3)

gameboard.SetCellValue(6, 3, 4)
gameboard.SetCellValue(7, 4, 7)

gameboard.SetCellValue(6, 6, 3)
gameboard.SetCellValue(6, 8, 6)
gameboard.SetCellValue(8, 6, 7)
gameboard.SetCellValue(8, 7, 4)
gameboard.SetCellValue(8, 8, 5)

gameboard.PrintBoardState()

print "Running solver"
if not gameboard.RecursiveSolve():
	print "Failed to solve!"
else:
	print "Solved!"

print gameboard.PrintBoardState()

