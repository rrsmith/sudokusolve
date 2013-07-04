#
# Build a board from an input file
#

from board import Board
import csv
import os.path
import math

# Create a gameboard from a csv file
# Expected format is a list of numbers per row, seperated by commas
# Value of 0 signifies an empty cell
def LoadFromFile(path):
	gameboard = Board()
		
	try:
		# check path for validity
		if os.path.isfile(path):
			with open(path, 'rb') as infile:
				gamerows = csv.reader(infile, delimiter=',')

				vals = []	

				for row in gamerows:
					rowv = []
					for cval in row:
						rowv.append(int(cval)) 
					vals.append(rowv)

				bsize = len(vals)
				gameboard.SetBoardSize(int(math.sqrt(bsize)))
				i = 0
				j = 0
				for row in vals:
					j = 0
					for cell in row:
						if cell != 0:
							gameboard.SetCellValue(i, j, cell)
						j += 1
					i += 1



		else:
			print "Not a file"
	except csv.Error as e:
		print "Read error: %s" % e

	return gameboard
