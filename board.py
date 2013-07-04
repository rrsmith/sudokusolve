#
# Sudoku board
#

from cell import Cell
import math

class Board:
	range = 3
	fullset = range * range

	cells = []

	rowset = []
	colset = []
	sqset = []
	
	solvedcells = 0
	solved = False

	def __init__(self):
		self.SetBoardSize(3)
		
	
	# Reset the board to size given by inrange
	def SetBoardSize(self, inrange):
		self.range = inrange
		self.fullset = self.range * self.range
		
		self.rowset = []
		self.colset = []
		self.sqset = []

		self.solvedcells = 0
		self.solved = False

		# Build the board
		for x in xrange(self.fullset):
			row = []
			for y in xrange(self.fullset):
				row.append(Cell())
			self.cells.append(row)
		
		# Fill the possibility sets
		tempset = range(1, self.fullset+1)

		for x in xrange(self.fullset):
			self.rowset.append(set(tempset))
			self.colset.append(set(tempset))
			self.sqset.append(set(tempset))

	
	# Get the appropriate set for a cell
	def GetSqrSetForCell(self, i, j):
		index = (int(math.floor((i / self.range))) * self.range) + int(math.floor((j / self.range)))
		return self.sqset[index]

	# Return the set of value possiblities for a cell
	def GetPossibilitiesForCell(self, i, j):
		return self.rowset[i] & self.colset[j] & self.GetSqrSetForCell(i, j)

	# Set the value for a cell
	def SetCellValue(self, i, j, value):
		self.cells[i][j].number = value
		self.rowset[i].discard(value)
		self.colset[j].discard(value)
		self.GetSqrSetForCell(i, j).discard(value)
		
		# print "Cell(%s, %s) set to %s" % (i, j, value)

		self.solvedcells += 1
		if self.solvedcells >= (self.fullset * self.fullset):
			self.solved = True

	# Returns true if a cell has only possiblity and been set to that
	def CheckCellForSinglePossibility(self, i, j):
		if self.cells[i][j].number is None:
			if len(self.GetPossibilitiesForCell(i, j)) == 1:
				self.SetCellValue(i, j, self.GetPossibilitiesForCell(i,j).pop())
				return True
			else:
				return False
		else:
			return False

	def PrintBoardState(self):
		line = "|"
		
		uline = "_" * (self.fullset * 4)
		print uline
		for i in xrange(self.fullset):
			for j in xrange(self.fullset):
				cval = " "
				if self.cells[i][j].number is not None:
					cval = self.cells[i][j].number
				line += " %s |" % cval
			print line
			print uline			
			line = "|"

	def PrintBoardAsCsv(self):
		output = ""
		for i in xrange(self.fullset):
			for j in xrange(self.fullset):
				cval = 0
				if self.cells[i][j].number is not None:
					cval = self.cells[i][j].number
				output += "%s" % cval
				if j < self.fullset - 1:
					output += ", "
			output += "\n"
		print output
					

	# Tactic #1
	# Check each cell to see if there is only one possibility for the value
	def SinglePossPass(self):
		result = False
		for i in xrange(self.fullset):
			for j in xrange(self.fullset):
				result |= self.CheckCellForSinglePossibility(i, j)
		return result

	# Tactic #2
	# Check each set to see particular values can only appear in one cell in the set
	def SetCheckPass(self):
		result = False
		# Rows
		for i in xrange(self.fullset):
			for x in xrange(1, self.fullset+1):
				colidexcoll = []
				for j in xrange(self.fullset):
					if self.cells[i][j].number is None:
						if x in self.GetPossibilitiesForCell(i, j):
							colidexcoll.append(j)
				if len(colidexcoll) == 1:
					self.SetCellValue(i, colidexcoll[0], x)
					result |= True
		
		# Columns
		for j in xrange(self.fullset):
			for x in xrange(1, self.fullset+1):
				rowidexcoll = []
				for i in xrange(self.fullset):
					if self.cells[i][j].number is None:
						if x in self.GetPossibilitiesForCell(i, j):
							rowidexcoll.append(i)
				if len(rowidexcoll) == 1:
					self.SetCellValue(rowidexcoll[0], j, x)
					result |= True


		return result

	# Attempt to solve, alternating between single possibliy check and set check
	def RecursiveSolve(self):
		if not self.solved:
			singlecount = 0
			setcheckcount = 0
			while self.SinglePossPass():
				singlecount += 1
			while self.SetCheckPass():
				setcheckcount += 1
			
			if singlecount + setcheckcount > 0:
				self.RecursiveSolve()
			else:
				if self.solved:
					return True
				else:
					return False
		else:
			return True


