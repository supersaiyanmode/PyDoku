import unittest
from nose.tools import assert_equal, assert_not_equal

from sudoku.cell import Cell

class CellTest(unittest.TestCase):
	
	def setUp(self):
		pass
		
	def test_value1(self):
		c = Cell((1,3), 0, 9)
		assert_equal(c.options, set())
		
	def test_value2(self):
		c = Cell((1,3), 0, None)
		assert_equal(c.options, set(range(1,10)))
	
	def test_display(self):
		c = Cell((4,8), 6, None)
		assert_equal(str(c), " ")
		assert_equal(repr(c), "%s: %s | %s"%(str((4,8)), "None",
					set(range(1,10))))
	
	def test_equality(self):
		c1 = Cell((1,3), 0, None)
		c2 = Cell((1,3), 1, None)
		
		assert_not_equal(c1, c2)