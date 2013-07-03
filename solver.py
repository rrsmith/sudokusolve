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

#poss = gameboard.GetPossibilitiesForCell(7, 7)
#print "Possibilities for 7, 7"
#for x in poss:
#	print "%s" % x

#poss = gameboard.GetPossibilitiesForCell(1, 1)
#print "Possibilities for 1, 1"
#for x in poss:
#	print "%s" % x

print "Running first pass"
gameboard.SinglePossPass()
gameboard.PrintBoardState()

for x in xrange(100):
	if not gameboard.solved:
		gameboard.SinglePossPass()
	else:
		print "Solved!"

print "Gameboard post single poss passes"
gameboard.PrintBoardState()

print "Running Set check pass"
gameboard.SetCheckPass()
gameboard.PrintBoardState()

for x in xrange(100):
	if not gameboard.solved:
		gameboard.SetCheckPass()
	else:
		print "Solved!"

print "Gameboard post set check passes"
gameboard.PrintBoardState()


