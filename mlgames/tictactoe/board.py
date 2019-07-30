from mlgames.board import Board

from copy import deepcopy

import numpy as np

IDENTITY_MATRIX = np.array([[1, 0], [0, 1]])
QUARTER_ROTATION_MATRIX = np.array([[0, 1], [-1, 0]])
Y_REFLECTION_MATRIX = np.array([[-1, 0], [0, 1]])
X_REFLECTION_MATRIX = np.array([[1, 0], [0, -1]])

def empty():
	return TicTacToeBoard([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']])

class TicTacToeBoard(Board):
	def __init__(self, board_state):
		self.board_state = board_state
		self.win_combinations = [
			[(0, 0), (0, 1), (0, 2)],
			[(1, 0), (1, 1), (1, 2)],
			[(2, 0), (2, 1), (2, 2)],
			[(0, 0), (1, 0), (2, 0)],
			[(0, 1), (1, 1), (2, 1)],
			[(0, 2), (1, 2), (2, 2)],
			[(0, 0), (1, 1), (2, 2)],
			[(0, 2), (1, 1), (2, 0)]
		]

	def play(self, piece, move):
		new_board_state = deepcopy(self.board_state)
		x, y = move
		if new_board_state[x][y] != '.':
			raise RuntimeError("({},{}) already occupied".format(x, y))
		new_board_state[x][y] = piece
		return TicTacToeBoard(new_board_state)

	def winner(self):
		for x in self.win_combinations:
			vals = [self.board_state[y[0]][y[1]]for y in x]
			if '.' not in vals and len(set(vals)) == 1:
				return vals[0]

		return None

	def parse_move(self, move_str):
		a, b = move_str.split(",")
		return int(a), int(b)

	def play_is_legal(self, piece, move):
		x, y = move
		return self.board_state[x][y] == '.'

	def all_legal_moves(self, piece):
		to_return = []
		for x in range(3):
			for y in range(3):
				move = (x, y)
				if self.play_is_legal(piece, move):
					to_return.append(move)
		return to_return

	def complete(self):
		for x in self.board_state:
			for y in x:
				if y == '.':
					return False
		return True

	def all_symmetries(self, move):
		def reflect_board_x():
			return TicTacToeBoard(transform_board(X_REFLECTION_MATRIX))

		def reflect_board_y():
			return TicTacToeBoard(transform_board(Y_REFLECTION_MATRIX))

		def rotate_board(number_of_rotations):
			return TicTacToeBoard(transform_board(compute_rotation_matrix(number_of_rotations)))

		def reflect_move_x(move):
			return transform_move(X_REFLECTION_MATRIX, move)

		def reflect_move_y(move):
			return transform_move(Y_REFLECTION_MATRIX, move)

		def rotate_move(move, number_of_rotations):
			return transform_move(compute_rotation_matrix(number_of_rotations), move)

		def transform_board(matrix):
			transforms = []
			for x in range(3):
				for y in range(3):
					transforms.append(([x, y], transform_move(matrix, [x, y])))

			new_board = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
			for old_position, new_position in transforms:
				new_board[new_position[0]][new_position[1]] = self.board_state[old_position[0]][old_position[1]]

			return new_board

		def transform_move(matrix, position):
			new_position = matrix.dot(np.array([position[0] - 1, position[1] - 1]))
			return (new_position[0] +  1, new_position[1] + 1)

		def compute_rotation_matrix(number_of_rotations):
			rotation_matrix = IDENTITY_MATRIX
			for i in range(number_of_rotations):
				rotation_matrix = QUARTER_ROTATION_MATRIX.dot(rotation_matrix)

			return rotation_matrix

		return [
			(reflect_board_x(), reflect_move_x(move)),
			(reflect_board_y(), reflect_move_y(move)),
			(rotate_board(1), rotate_move(move, 1)),
			(rotate_board(2), rotate_move(move, 2)),
			(rotate_board(3), rotate_move(move, 3)),
		]

	def __str__(self):
		string = ""
		for x in self.board_state:
			for y in x:
				string += y
			string += '\n'
		return string

	def to_single_line_string(self):
		return "".join(["".join(x) for x in self.board_state])
