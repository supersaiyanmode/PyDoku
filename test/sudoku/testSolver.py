import unittest
from nose.tools import assert_equal, assert_not_equal

from sudoku.cell import Cell
from sudoku.board import Board
from sudoku.solver import Solver
from main import readSudokuFile

class SolverTest(unittest.TestCase):
	
	def setUp(self):
		pass
		
	def test_value1(self):
		board = Board(readSudokuFile("test-input/test-input.txt"))
		print repr(Solver.getAffectedCells(board, board[(7,1)]))
		#No asserts, stdout check
		
	def test_invalid(self):
		print "------"
		board = Board(readSudokuFile("test-input/test-invalid1.txt"))
		print "Board:"
		print board
		print "Checking for: ", repr(board[(0,6)]), "$"
		res = Solver.getAffectedFilledCells(board,board[(0,6)])
		print "Final:", repr(res)
		if len(set(res)) != len(res):
			raise InvalidSudokuStateError("Cell @" + repr(cell))
		print "-------"
		#No asserts, stdout check