from itertools import chain
from collections import defaultdict
import sys
from copy import deepcopy

from cell import Cell
from board import Board

from exception.sudoku import SudokuValueError
from exception.sudoku import InvalidSudokuStateError

class Solver(object):
	def __init__(self, board):
		self.board = board
		
	def solve(self):
		while True:
			Solver.assertValidState(self.board)
			
			Solver.reCalculatePossibilities(self.board)
			remainingCells = Solver.getRemainingCells(self.board)
			initialRemainingCells = len(remainingCells)
			print "Initial: " , initialRemainingCells
			Solver.checkUniquePossibilities(self.board)
			
			Solver.startGuess(self.board)
			
			finalRemainingCells = len(Solver.getRemainingCells(self.board))
			print "Final: " , finalRemainingCells
			if initialRemainingCells == finalRemainingCells:
				break
	
	@staticmethod
	def assertValidState(board):
		"""Check for valid state of the board. Throw Error otherwise."""
		for num in range(board.ROWS):
			res = [x.value for x in board.getCellsInRow(num) if x.value]
			if len(set(res)) != len(res):
				raise InvalidSudokuStateError("Row number:%d"%num)
		for num in range(board.COLS):
			res = [x.value for x in board.getCellsInCol(num) if x.value]
			if len(set(res)) != len(res):
				raise InvalidSudokuStateError("Col number:%d"%num)
				
		gridCount= board.ROWS / board.GRID_SIZE * board.COLS / board.GRID_SIZE
		for num in range(gridCount):
			res = [x.value for x in board.getCellsInGrid(num) if x.value]
			if len(set(res)) != len(res):
				raise InvalidSudokuStateError("Grid number:%d"%num)
				
	
	@staticmethod
	def reCalculatePossibilities(board):
		"""Refresh the possibility set for all cells in the board."""
		gridCount= board.ROWS / board.GRID_SIZE * board.COLS / board.GRID_SIZE
		
		rows = [board.getCellsInRow(i) for i in range(board.ROWS)]
		cols = [board.getCellsInCol(i) for i in range(board.COLS)]
		grids= [board.getCellsInGrid(i) for i in range(gridCount)]
		
		rowValues = [
			{cell.value for cell in row if cell.value}
			for row in rows
		]
		colValues = [
			{cell.value for cell in col if cell.value}
			for col in cols
		]
		
		gridValues = [
			{cell.value for cell in grid if cell.value}
			for grid in grids
		]
		
		for rowNum, row in enumerate(rows):
			for colNum, cell in enumerate(row):
				cell.options = (cell.options -
								rowValues[rowNum] -
								colValues[colNum] -
								gridValues[board.getGridIndex(rowNum, colNum)])
	
	@staticmethod
	def checkUniquePossibilities(board):
		"""Go over each cell, form constained region, and try to assign values,
		if appropriate.
		"""
		cellsFixed = []
		for row in board.cells:
			for cell in row:
				#affectedCells = Solver.getAffectedCells(board,cell)
				cellRows = board.getCellsInRow(cell)
				cellCols = board.getCellsInCol(cell)
				cellGrid = board.getCellsInGrid(cell)
				
				cellsFixed += Solver.fixUniquePossibilities(board, cellRows)
				cellsFixed += Solver.fixUniquePossibilities(board, cellCols)
				cellsFixed += Solver.fixUniquePossibilities(board, cellGrid)
		return cellsFixed
	
	@staticmethod
	def getRemainingCells(board):
		"""Returns a list of all un-filled cells in the board."""
		res = []
		for row in board.cells:
			for cell in row:
				if cell.value is None:
					res.append(cell)
		return res
	
	@staticmethod
	def getAffectedCells(board,cell): #Better name?
		"""Returns a list of all cells in the constrained region that are
		not filled.
		"""
		cells = list(set(
			board.getCellsInRow(cell) +
			board.getCellsInCol(cell) +
			board.getCellsInGrid(cell)
		))
		return filter(lambda x: not x.value, cells)
	
	@staticmethod
	def getAffectedFilledCells(board,cell): #Better name?
		"""Returns a list of all cells in the constrained region that are
		filled.
		"""
		cells = list(set(
			board.getCellsInRow(cell) +
			board.getCellsInCol(cell) +
			board.getCellsInGrid(cell)
		))
		
		return filter(lambda x: x.value, cells)
		
	@staticmethod
	def fixUniquePossibilities(board, cells):
		"""Check the constrained area surrounding the cell. Fix cell value if
		appropriate
		"""
		fixedCells = []
		uniques = defaultdict(set)
		for cell in cells:
			for possib in cell.options:
				uniques[possib].add(cell)
		
		for possibValue, setOfCells in uniques.items():
			if len(setOfCells) == 1:
				cell = setOfCells.pop()
				cell.options = set()
				cell.value = possibValue
				print "Fixing:", repr(cell)
				affectedCells = Solver.getAffectedCells(board, cell)
				Solver.removePossibilities(affectedCells, possibValue)
				fixedCells.append(cell)
		return fixedCells
		
	@staticmethod
	def removePossibilities(cells, value):
		for cell in cells:
			try:
				cell.options.remove(value)
			except KeyError, e:
				pass

	@staticmethod
	def startGuess(board):
		boardCopy = deepcopy(board)
		
		
		
