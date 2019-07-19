from mlgames.board import Board

import numpy as np

Y_REFLECTION_MATRIX = np.array([[1, 0], [0, -1]])

BOARD_HEIGHT = 6
BOARD_WIDTH = 7

def empty():
	arr = np.chararray([BOARD_HEIGHT, BOARD_WIDTH])
	arr.fill('.')
	return Connect4Board(arr)

# Connect 4 board, 6 rows & 7 columns
# a 'move' is simply a column, the piece slides down to the lowest non-taken position in that column
class Connect4Board(Board):
	def __init__(self, board_state):
		self.board_state = board_state

	def play(self, piece, move):
		new_board_state = self.board_state.copy()
		row = BOARD_HEIGHT - 1
		while (new_board_state[row][move] != b'.') and row >= 0:
			row = row - 1
		if row < 0:
			raise RuntimeError("({}) is full!".format(move, row))
		new_board_state[row][move] = piece.encode('ascii')
		return Connect4Board(new_board_state)

	def winner(self):
		def contains_continuous(arr):
			last_seen = None
			number_seen = 0
			for x in arr:
				if x == last_seen:
					number_seen += 1
				else:
					last_seen = x
					number_seen = 1
				if number_seen == 4 and last_seen != b'.':
					return last_seen

		for x in range(BOARD_HEIGHT):
			potential = contains_continuous(self.board_state[x, :])
			if potential:
				return potential.decode("ascii")

		for x in range(BOARD_WIDTH):
			potential = contains_continuous(self.board_state[:, x])
			if potential:
				return potential.decode("ascii")

		y_reflected = self.reflect_board_y()
		for x in range(-2, 4):
			potential = contains_continuous(self.board_state.diagonal(x))
			if potential:
				return potential.decode("ascii")

			potential = contains_continuous(y_reflected.board_state.diagonal(x))
			if potential:
				return potential.decode("ascii")

		return None

	def play_is_legal(self, piece, move):
		return self.board_state[0][move] == b'.'

	def complete(self):
		for x in self.board_state:
			for y in x:
				if y == b'.':
					return False
		return True

	def reflect_board_y(self):
			return Connect4Board(self.transform_board(Y_REFLECTION_MATRIX))

	def transform_board(self, matrix):
		transforms = []
		for col in range(BOARD_WIDTH):
			for row in range(BOARD_HEIGHT):
				transforms.append(([row, col], self.transform_position(matrix, [row, col])))

		new_board = empty()
		for old_position, new_position in transforms:
			new_board.board_state[new_position[0]][new_position[1]] = self.board_state[old_position[0]][old_position[1]]

		return new_board.board_state

	def transform_position(self, matrix, position):
		new_position = matrix.dot(np.array([position[0], position[1] - 3]))
		return [new_position[0], new_position[1] + 3]

	def all_symmetries(self, move):
		def reflect_move_y(move):
			return self.transform_position(Y_REFLECTION_MATRIX, [0, move])

		return [(self.reflect_board_y(), reflect_move_y(move)[1])]
	
	def __str__(self):
		string = ""
		for x in self.board_state:
			for y in x:
				string += y.decode("ascii")
			string += '\n'
		return string

	def to_single_line_string(self):
		return "".join(["".join([y.decode("ascii") for y in x]) for x in self.board_state])
