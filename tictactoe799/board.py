from copy import deepcopy

import numpy as np

IDENTITY_MATRIX = np.array([[1, 0], [0, 1]])
QUARTER_ROTATION_MATRIX = np.array([[0, 1], [-1, 0]])
Y_REFLECTION_MATRIX = np.array([[-1, 0], [0, 1]])
X_REFLECTION_MATRIX = np.array([[1, 0], [0, -1]])

class Board:
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

	def place(self, piece, x, y):
		new_board_state = deepcopy(self.board_state)
		if new_board_state[x][y] != '.':
			raise RuntimeError("({},{}) already occupied".format(x, y))
		new_board_state[x][y] = piece
		return Board(new_board_state)

	def taken(self, x, y):
		return self.board_state[x][y] != '.'

	def value(self, x, y):
		return self.board_state[x][y]

	def winner(self):
		for x in self.win_combinations:
			vals = [self.board_state[y[0]][y[1]]for y in x]
			if '.' not in vals and len(set(vals)) == 1:
				return vals[0]

		return None

	def full(self):
		for x in self.board_state:
			for y in x:
				if y == '.':
					return False
		return True

	def reflect_board_x(self):
		return Board(self.transform_board(X_REFLECTION_MATRIX))

	def reflect_board_y(self):
		return Board(self.transform_board(Y_REFLECTION_MATRIX))

	def rotate_board(self, number_of_rotations):
		return Board(self.transform_board(self.compute_rotation_matrix(number_of_rotations)))

	def reflect_position_x(self, position):
		return self.transform_position(X_REFLECTION_MATRIX, position)

	def reflect_position_y(self, position):
		return self.transform_position(Y_REFLECTION_MATRIX, position)

	def rotate_position(self, position, number_of_rotations):
		return self.transform_position(self.compute_rotation_matrix(number_of_rotations), position)

	def transform_board(self, matrix):
		transforms = []
		for x in range(3):
			for y in range(3):
				transforms.append(([x, y], self.transform_position(matrix, [x, y])))

		new_board = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
		for old_position, new_position in transforms:
			new_board[new_position[0]][new_position[1]] = self.board_state[old_position[0]][old_position[1]]

		return new_board

	def transform_position(self, matrix, position):
		new_position = matrix.dot(np.array([position[0] - 1, position[1] - 1]))
		return [new_position[0] +  1, new_position[1] + 1]

	def compute_rotation_matrix(self, number_of_rotations):
		rotation_matrix = IDENTITY_MATRIX
		for i in range(number_of_rotations):
			rotation_matrix = QUARTER_ROTATION_MATRIX.dot(rotation_matrix)

		return rotation_matrix

	def __str__(self):
		string = ""
		for x in self.board_state:
			for y in x:
				string += y
			string += '\n'
		return string

	def to_numerical_grid(self):
		def translate(val):
			return 2 if val == 'O' else 1 if val == 'X' else 0
		return [[translate(a) for a in b] for b in self.board_state]

	def to_single_line_string(self):
		return "".join(["".join(x) for x in self.board_state])
