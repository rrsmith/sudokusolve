#
# Sudoku board of arbitrary square size
#

from cell import Cell
import math

class Board:
	## Square set size of board
	range = 3
	## Possible value count for a single set
	fullset = range * range

	## The set of cells on the board
	cells = []

	## Remaining possibility sets for rows 
	rowset = []
	## Remaining possiblity sets for columns
	colset = []
	## Remaining possiblity sets for square sets
	sqset = []
	
	usedpositions = []

	## Number of cells solved
	solvedcells = 0
	## Is board solved (all cells have a value)
	solved = False
	ignorepositioncheck = True	

	## Board defaults to a square size of 3 (A standard board)
	def __init__(self):
		self.SetBoardSize(3)
		
	## Reset the board to square size given by inrange
	# @param inrange New square size
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
			self.usedpositions.append(set())
			for y in xrange(self.fullset):
				row.append(Cell())
			self.cells.append(row)
		
		# Fill the possibility sets
		tempset = range(1, self.fullset+1)

		for x in xrange(self.fullset):
			self.rowset.append(set(tempset))
			self.colset.append(set(tempset))
			self.sqset.append(set(tempset))

	## Get the index of the sqr set for a cell
	# @param i Row index
	# @param j Column index
	def GetSqrSetIndex(self, i, j):
		index = (int(math.floor((i / self.range))) * self.range) + int(math.floor((j / self.range)))
		return index

	## Get the possibility set of the sqr set of a cell
	# @param i Row index
	# @param j Column index
	def GetSqrSetForCell(self, i, j):
		index = self.GetSqrSetIndex(i, j)
		return self.sqset[index]

	# Return the set of value possiblities for a cell
	def GetPossibilitiesForCell(self, i, j):
		baseset = (self.rowset[i] & self.colset[j] & self.GetSqrSetForCell(i, j))
		if not self.ignorepositioncheck:
			baseset -= self.GetPositionalSetForCell(i, j)
		return baseset

	# Set the value for a cell
	def SetCellValue(self, i, j, value):
		"""Set the value for a cell."""
		self.cells[i][j].number = value
		self.rowset[i].discard(value)
		self.colset[j].discard(value)
		self.GetSqrSetForCell(i, j).discard(value)
		self.GetPositionalSetForCell(i, j).add(value)

		self.solvedcells += 1
		if self.solvedcells >= (self.fullset * self.fullset):
			self.solved = True

	# Get the position of a cell relative to its sqr set
	def GetRelativeCellPosition(self, i, j):
		"""Return the position of a cell relative to its square set."""
		pos = []
		outi = i % self.range
		outj = j % self.range
		pos.append(outi)
		pos.append(outj)

		return pos

	def GetPositionalSetForCell(self, i, j):
		pos = self.GetRelativeCellPosition(i, j)
		index = (pos[0] * self.range) + pos[1]
		return self.usedpositions[index]

	# Returns true if a cell has only possiblity and been set to that
	def CheckCellForSinglePossibility(self, i, j):
		"""Checks a cell to see if it has only one possible value and sets it if so.
		Returns True if set.
		"""
		if self.cells[i][j].number is None:
			if len(self.GetPossibilitiesForCell(i, j)) == 1:
				self.SetCellValue(i, j, self.GetPossibilitiesForCell(i,j).pop())
				return True
			else:
				return False
		else:
			return False

	def PrintBoardState(self):
		"""Print the board state in a (mostly) human readable format."""
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
		"""Print the board state in a format suitable for csv files."""
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
		"""Tactic #1
		Check each cell to see if there is only one possibility for the value.
		"""
		result = False
		for i in xrange(self.fullset):
			for j in xrange(self.fullset):
				result |= self.CheckCellForSinglePossibility(i, j)
		return result

	# Tactic #2
	# Check each set to see if any values can only appear in one cell in the set
	# Checking rows, columns then sqr sets
	def SetCheckPass(self):
		"""Tactic #2
		Check each set to see if any values can only appear in one cell in the set.
		"""
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


		# Sqr sets
		for k in xrange(self.fullset):
			offseti = int(math.floor(k / self.range)) * self.range
			offsetj = (k % self.range) * self.range
			for x in xrange(1, self.fullset+1):
				cellcoll = []
				for i in xrange(offseti, offseti+self.range):
					for j in xrange(offsetj, offsetj+self.range):
						if self.cells[i][j].number is None:
							if x in self.GetPossibilitiesForCell(i, j):
								cellloc = [i, j]
								cellcoll.append(cellloc)
				if len(cellcoll) == 1:
					self.SetCellValue(cellcoll[0][0], cellcoll[0][1], x)
					result |= True


		return result


	# Attempt to solve, alternating between single possibliy check and set check
	def Solve(self):
		"""
		Attempts to solve the board.
		"""
		if not self.solved:
			singlecount = 0
			setcheckcount = 0
			while self.SinglePossPass():
				singlecount += 1
			while self.SetCheckPass():
				setcheckcount += 1
			
			if singlecount + setcheckcount > 0:
				return self.Solve()
			else:
				return self.solved
		else:
			return True


