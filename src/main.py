from sudoku.board import Board
from sudoku.solver import Solver

def readSudokuFile(filePath):
	toVal = lambda x: None if x.strip() == "_" else int(x)
	with open(filePath) as f:
		return [map(toVal,line.strip().split()) for line in f]


def main():
	board = Board(readSudokuFile('input.txt'))
	solver = Solver(board)
	solver.solve()
	#print "Final --"
	#print repr(board)
	print "-----"
	solver.solve()
	print board

if __name__ == '__main__':
	main()