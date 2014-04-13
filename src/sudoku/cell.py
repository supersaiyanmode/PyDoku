from exception.sudoku import SudokuValueError

class Cell(object):
	def __init__(self, position, gridIndex, value):
		"""A new cell object
		position  - A tuple in the form of (rowNum, colNum)
		gridIndex - Grid Index. Check Board.getGridIndex(..)
		value     - A number if the cell is filled. None otherwise
		"""
		if value and type(value) != type(0):
			raise SudokuValueError("Invalid type of value.")
		
		if value and 0 > value > 9:
			raise SudokuValueError("Invalid value for cell: %d"%value)
		
		if type(position) != tuple or len(position) != 2:
			raise SudokuValueError("Invalid position for cell.")
		
		self.value = value
		self.position = position
		self.gridIndex = gridIndex
		self.options = set() if value else set(range(1,10))
		self.dependantCells = []
		#print "Cell:",vars(self)
		
	
	def __eq__(self, other):
		"""Two cells are equal if their positions are same"""
		return self.position == other.position
	
	def __hash__(self):
		return hash(self.position)
	
	def __str__(self):
		return str(self.value) if self.value else " "
	
	def __repr__(self):
		return "%s: %s | %s"%(str(self.position), str(self.value),
					str(self.options)) 