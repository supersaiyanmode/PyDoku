from itertools import chain

from cell import Cell

from exception.sudoku import SudokuValueError

class Board(object):
	COLS = 9
	ROWS = 9
	GRID_SIZE = 3
	
	def __init__(self, startState):
		"""Construct a board from a startState.
		
		startState - A 2D array that contains either number or None
		
		throws SudokuValueError in case of invalid types or rows/columns count.
		"""
		if type(startState) != type([]) and type(startState[0]) != type([]):
			raise SudokuValueError("Invalid type passed for startState.")
		if len(startState) != self.ROWS:
			raise SudokuValueError("Invalid number of rows.")
		if any(len(row) != self.COLS for row in startState):
			raise SudokuValueError("Invalid number of Columns for some rows.")
			
		self.cells = [[
				Cell((rowNum,colNum), self.getGridIndex(rowNum, colNum), val)
				for colNum, val in enumerate(row)
			]
			for rowNum, row in enumerate(startState)
		]
		
	def __getitem__(self, position):
		"""Retrieve cell by the position tuple."""
		if type(position) != tuple or len(position) != 2:
			raise AttributeError("Invalid type.")
		if 0 <= position[0] < Board.ROWS and 0<= position[1] < Board.COLS:
			return self.cells[position[0]][position[1]]
		raise AttributeError("Invalid Position:" + str(position))
	
	def __str__(self):
		"""Put the separator char in between. Assumes 9 * 9 grid."""
		ins = lambda x, c: x[:3] + [c] + x[3:6] + [c] + x[6:]
		return "\n".join(" ".join(str(cell) for cell in ins(row,"|"))
							for row in ins(self.cells,["-"]*9))
	
	def __repr__(self):
		return "\n".join("\n".join(repr(cell) for cell in row) for row in
							self.cells)
	
	def getGridIndex(self, rowNum, colNum):
		"""Retrieves the grid index.
		rowNum - row number of from [0,Board.ROWS)
		colNum - column number of from [0,Board.COLS)
		
		If in the below, each cell represent a GRID (3*3), then the indices are:
		012
		345
		678
		"""
		return (self.GRID_SIZE*int(rowNum/self.GRID_SIZE) +
					int(colNum/self.GRID_SIZE))
	
	def getCellsInGrid(self, obj):
		"""Returns a list of all cells in a grid identified by either:
		 obj (int)  - Returns cells by grid index
		 obj (Cell) - Returns cells by another cell instance
		"""
		if isinstance(obj,int):
			rowsMin = self.GRID_SIZE * int(obj/self.GRID_SIZE)
			rowsMax = self.GRID_SIZE * (int(obj/self.GRID_SIZE)+1)
			colsMin = self.GRID_SIZE * (obj%self.GRID_SIZE)
			colsMax = self.GRID_SIZE * ((obj%self.GRID_SIZE)+1)
			res = []
			for rows in self.cells[rowsMin:rowsMax]:
				res += rows[colsMin:colsMax]
			return res
		elif isinstance(obj, Cell):
			return self.getCellsInGrid(self.getGridIndex(
				obj.position[0],obj.position[1]))
	
	def getCellsInRow(self, obj):
		"""Returns a list of all cells in a row identified by either:
		 obj (int)  - Returns cells by row index
		 obj (Cell) - Returns cells by another cell instance
		"""
		if isinstance(obj, int):
			return self.cells[obj]
		elif isinstance(obj, Cell):
			return self.getCellsInRow(obj.position[0])
			
	def getCellsInCol(self, obj):
		"""Returns a list of all cells in a column identified by either:
		 obj (int)  - Returns cells by column index
		 obj (Cell) - Returns cells by another cell instance
		"""
		if isinstance(obj, int):
			return [row[obj] for row in self.cells]
		elif isinstance(obj, Cell):
			return self.getCellsInCol(obj.position[1])
		
		


