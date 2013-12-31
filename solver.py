#!/usr/bin/python
from cell import Cell
from board import Board
import argparse
import boardfromtext


parser = argparse.ArgumentParser(description='Sudoku solver.')
parser.add_argument('infile', help='A csv of game information')

args = parser.parse_args()

gameboard = boardfromtext.LoadFromFile(args.infile)

gameboard.PrintBoardState()

print "Running solver"
if not gameboard.Solve():
	print "Failed to solve!"
else:
	print "Solved!"

print gameboard.PrintBoardState()

