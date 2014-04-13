import unittest
from nose.tools import assert_equal

from sudoku.board import Board
from sudoku.cell import Cell
from main import readSudokuFile

class BoardTest(unittest.TestCase):
	
	def setUp(self):
		pass
		
	def test_value1(self):
		board = Board([[None]*Board.COLS]*Board.ROWS)
		res = 	([[0,0,0,1,1,1,2,2,2]]*3 +
				[[3,3,3,4,4,4,5,5,5]]*3 +
				[[6,6,6,7,7,7,8,8,8]]*3)
		for i in range(Board.ROWS):
			for j in range(Board.COLS):
				assert_equal(board.getGridIndex(i,j),res[i][j])
				
	def test_getItem(self):
		board = Board(readSudokuFile("test-input/test-input.txt"))
		assert_equal(board[(2,8)],Cell((2,8),2,7))
		
	def test_getCellsInGrid(self):
		board = Board(readSudokuFile("test-input/test-input.txt"))
		for i in range(9):
			print "For %d"%i
			print repr(board.getCellsInGrid(i))
	