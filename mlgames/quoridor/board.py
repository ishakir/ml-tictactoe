from mlgames.board import Board

import numpy as np

BOARD_SIZE = 9
STARTING_WALLS = 10

def a(arr):
	return np.array(arr)

ALLOWED_PLAYER_MOVE_DIFFS = [
	a([0, 1]),
	a([1, 0]),
	a([0, -1]),
	a([-1, 0])
]

ONLY_ALLOWED_IF_PLAYER_INBETWEEN_DIFFS = [
	a([0, 2]),
	a([2, 0]),
	a([0, -2]),
	a([-2, 0])
]

ALLOWED_WALL_START_END_DIFFS = [
	a([0, 2]),
	a([2, 0])
]

def empty():
	x_position = a([8, 4])
	o_position = a([0, 4])
	wall_positions = list()
	return QuoridorBoard(x_position, STARTING_WALLS, None, o_position, STARTING_WALLS, None, wall_positions)

class NodeChain():
	def __init__(self, route, current):
		self.route = route
		self.current = current

# TODO Implementation is missing corner case where you can jump an opponent to left or right if 
# umping straight over is impossilbe, sigh. Board so compilcated :(
class QuoridorBoard(Board):
	def __init__(self, x_position, x_remaining_walls, x_route_to_home_guess, o_position, o_remaining_walls, o_route_to_home_guess, wall_positions):
		self.x_position = x_position
		self.x_remaining_walls = x_remaining_walls
		self.o_position = o_position
		self.o_remaining_walls = o_remaining_walls
		self.wall_positions = wall_positions

		if x_route_to_home_guess is None:
			self.x_route_to_home = self.route_to_row(x_position, 0, wall_positions)
		elif not np.array_equal(self.x_position, x_route_to_home_guess[0]):
			if np.array_equal(self.x_position, x_route_to_home_guess[1]):
				self.x_route_to_home = x_route_to_home_guess[1:]
			else:
				self.x_route_to_home = self.route_to_row(x_position, 0, wall_positions)
		elif self.route_is_broken(x_route_to_home_guess, wall_positions):
			self.x_route_to_home = self.route_to_row(x_position, 0, wall_positions)
		else:
			self.x_route_to_home = x_route_to_home_guess

		if o_route_to_home_guess is None:
			self.o_route_to_home = self.route_to_row(o_position, BOARD_SIZE - 1, wall_positions)
		elif not np.array_equal(self.o_position, o_route_to_home_guess[0]):
			if np.array_equal(self.o_position, o_route_to_home_guess[1]):
				self.o_route_to_home = o_route_to_home_guess[1:]
			else:
				self.o_route_to_home = self.route_to_row(o_position, BOARD_SIZE - 1, wall_positions)
		elif self.route_is_broken(o_route_to_home_guess, wall_positions):
			self.o_route_to_home = self.route_to_row(o_position, BOARD_SIZE - 1, wall_positions)
		else:
			self.o_route_to_home = o_route_to_home_guess


	# A play takes two forms:
	# 1. ('P', 0, 1) - Which encodes: Move the player to (0, 1)
	# 2. ('W', (0, 1), (0, 3)) - Place a wall starting at (0, 1) and ending at (0, 3)
	def play(self, piece, move):
		if not self.play_is_legal(piece, move):
			raise ValueError("Unable to play move! {}".format(str(move)))

		move_type = move[0]
		if move_type == 'P':
			if piece == 'X':
				return QuoridorBoard(move[1], self.x_remaining_walls, self.x_route_to_home, self.o_position, self.o_remaining_walls, self.o_route_to_home, self.wall_positions)
			elif piece == 'O':
				return QuoridorBoard(self.x_position, self.x_remaining_walls, self.x_route_to_home, move[1], self.o_remaining_walls, self.o_route_to_home, self.wall_positions)
			else:
				raise ValueError("Don't recognize piece {}".format(piece))
		elif move_type == 'W':
			if piece == 'X':
				return QuoridorBoard(self.x_position, self.x_remaining_walls - 1, self.x_route_to_home, self.o_position, self.o_remaining_walls, self.o_route_to_home, self.wall_positions + [move[1:]])
			elif piece == 'O':
				return QuoridorBoard(self.x_position, self.x_remaining_walls, self.x_route_to_home, self.o_position, self.o_remaining_walls - 1, self.o_route_to_home, self.wall_positions + [move[1:]])
			else:
				raise ValueError("Don't recognize piece {}".format(piece))
		else:
			raise ValueError("Don't recognize move type {}".format(move_type))

	def winner(self):
		if self.x_position[0] == 0:
			return 'X'
		elif self.o_position[0] == BOARD_SIZE - 1:
			return 'O'
		else:
			return None

	def parse_move(self, move_str):
		split = move_str.split()
		if split[0] == 'P':
			return ('P', a([int(split[1]), int(split[2])]))
		elif split[0] == 'W':
			start_split = split[1].split(",")
			end_split = split[2].split(",")
			return ('W', a([int(start_split[0]), int(start_split[1])]), a([int(end_split[0]), int(end_split[1])]))
		else:
			raise ValueError("Didn't understand move_type {}".format(split[0]))

	def contains(self, l1, l2):
		for x in l1:
			for y in l2:
				if np.array_equal(x, y):
					return True
		return False

	def is_on_board(self, arr):
		return arr[0] >= 0 and arr[0] < BOARD_SIZE and arr[1] >= 0 and arr[1] < BOARD_SIZE

	def is_legal_wall_start_or_end(self, arr):
		return arr[0] >= 0 and arr[0] <= BOARD_SIZE and arr[0] >= 0 and arr[1] <= BOARD_SIZE

	def has_wall_inbetween(self, start, end, walls):
		diff = end - start
		if diff[0] != 0 and diff[1] != 0:
			raise ValueError("Invalid diff between {} and {}".format(start, end))

		is_horizontal = diff[0] == 0

		possible_blocking_walls = []
		if is_horizontal:
			player_columns = [start[1], end[1]]
			player_row = start[0]
			relevant_wall_columns = [x for x in range(min(player_columns) + 1, max(player_columns) + 1)]
			for col in relevant_wall_columns:
				possible_blocking_walls.append([a([player_row - 1, col]), a([player_row + 1, col])])
				possible_blocking_walls.append([a([player_row, col]), a([player_row + 2, col])])
		else:
			player_rows = [start[0], end[0]]
			player_column = start[1]
			relevant_wall_rows = [x for x in range(min(player_rows) + 1, max(player_rows) + 1)]
			for row in relevant_wall_rows:
				possible_blocking_walls.append([a([row, player_column - 1]), a([row, player_column + 1])])
				possible_blocking_walls.append([a([row, player_column]), a([row, player_column + 2])])

		return self.contains(possible_blocking_walls, walls)

	def route_to_row(self, start, row_to_reach, walls):
		encountered = set()
		to_explore = list()

		to_explore.append(NodeChain([], start))
		while len(to_explore) != 0:
			current_node = to_explore.pop(0)

			if current_node.current[0] == row_to_reach:
				return current_node.route + [current_node.current]

			encountered.add(str(current_node.current))
			for diff in ALLOWED_PLAYER_MOVE_DIFFS:
				next = NodeChain(current_node.route + [current_node.current], current_node.current + diff)
				if self.is_on_board(next.current) and not self.has_wall_inbetween(current_node.current, next.current, walls) and str(next.current) not in encountered:
					to_explore.append(next)

		return None

	def route_is_broken(self, route, walls):
		for i in range(len(route) - 1):
			start, end = route[i], route[i + 1]
			if self.has_wall_inbetween(start, end, walls):
				return True
		return False

	def row_is_reachable(self, piece, start, row_to_reach, walls):
		current_route = self.x_route_to_home if piece == 'X' else self.o_route_to_home

		if not self.route_is_broken(current_route, walls):
			return True
		else:
			return self.route_to_row(start, row_to_reach, walls) is not None

	def play_is_legal(self, piece, move):
		move_type = move[0]
		if move_type == 'P':
			proposed_position = move[1]
			if not self.is_on_board(proposed_position):
				return False

			current_position = self.x_position if piece == 'X' else self.o_position
			opponent_position = self.o_position if piece == 'X' else self.x_position

			if self.has_wall_inbetween(current_position, proposed_position, self.wall_positions):
				return False

			# Check that we're only moving one square
			diff = proposed_position - current_position
			if not self.contains([diff], ALLOWED_PLAYER_MOVE_DIFFS) and not self.contains([diff], ONLY_ALLOWED_IF_PLAYER_INBETWEEN_DIFFS):
				return False
			elif self.contains([diff], ONLY_ALLOWED_IF_PLAYER_INBETWEEN_DIFFS):
				# Work out if the player is indeed inbetween
				middle_diff = diff / 2
				expected_opponent_position = current_position + middle_diff
				return np.array_equal(expected_opponent_position, opponent_position)
			else:
				# Finally check that we're not trying to place directly on top of opponent
				return not np.array_equal(proposed_position, opponent_position)
		elif move_type == 'W':
			remaining_walls = self.x_remaining_walls if piece == 'X' else self.o_remaining_walls
			if remaining_walls <= 0:
				return False

			wall_start, wall_end = move[1], move[2]

			# Check the wall is on the board
			if not self.is_legal_wall_start_or_end(wall_start) or not self.is_legal_wall_start_or_end(wall_end):
				return False

			# Check the wall has the correct orientation and length
			diff = wall_end - wall_start
			if not self.contains([diff], ALLOWED_WALL_START_END_DIFFS):
				return False

			# Check that wall space is not already occupied
			is_horizontal = diff[0] != 0
			possible_intersectors = []
			possible_intersectors.append([wall_start, wall_end])
			if is_horizontal:
				possible_intersectors.append([wall_start + a([1, 0]), wall_end + a([1, 0])])
				possible_intersectors.append([wall_start - a([1, 0]), wall_end - a([1, 0])])
				possible_intersectors.append([wall_start + a([1, -1]), wall_start + a([1, 1])])
			else:
				possible_intersectors.append([wall_start + a([0, 1]), wall_end + a([0, 1])])
				possible_intersectors.append([wall_start - a([0, 1]), wall_end - a([0, 1])])
				possible_intersectors.append([wall_start + a([-1, 1]), wall_start + a([1, 1])])

			if self.contains(possible_intersectors, self.wall_positions):
				return False

			# Finally check players have a route to the end
			if not self.row_is_reachable(piece, self.x_position, 0, self.wall_positions + [move[1:]]):
				return False

			if not self.row_is_reachable(piece, self.o_position, BOARD_SIZE - 1, self.wall_positions + [move[1:]]):
				return False

			return True
		else:
			raise ValueError("Unknown move type: {}".format(move_type))

	def all_legal_moves(self, piece):
		all_possible_moves = []

		player_position = self.x_position if piece == 'X' else self.o_position

		for move in (ALLOWED_PLAYER_MOVE_DIFFS + ONLY_ALLOWED_IF_PLAYER_INBETWEEN_DIFFS):
			new_position = player_position + move
			all_possible_moves.append(['P', new_position])

		for row in range(BOARD_SIZE + 1):
			for col in range(BOARD_SIZE):
				wall_start = a([row, col])
				wall_end = a([row, col + 2])
				all_possible_moves.append(['W', wall_start, wall_end])

		for col in range(BOARD_SIZE + 1):
			for row in range(BOARD_SIZE):
				wall_start = a([row, col])
				wall_end = a([row + 2, col])
				all_possible_moves.append(['W', wall_start, wall_end])

		return [m for m in all_possible_moves if self.play_is_legal(piece, m)]

	# We have no draw state
	def complete(self):
		return False

	def all_symmetries(self, move):
		raise ValueError("Not yet implemented")

	def __str__(self):
		board_print_size = (2 * BOARD_SIZE) + 1
		char_array = [[' ' for x in range(board_print_size)] for x in range(board_print_size)]

		for x in range(0, board_print_size + 1, 2):
			for y in range(0, board_print_size + 1, 2):
				char_array[x][y] = '+'

		board_x_pos = (2 * self.x_position) + 1
		board_o_pos = (2 * self.o_position) + 1

		char_array[board_x_pos[0]][board_x_pos[1]] = 'X'
		char_array[board_o_pos[0]][board_o_pos[1]] = 'O'

		for wall in self.wall_positions:
			board_wall_start = wall[0] * 2
			board_wall_end = wall[1] * 2

			diff = (board_wall_end - board_wall_start) // 4
			is_horizontal = diff[0] == 0

			pos = board_wall_start
			while not np.array_equal(pos, board_wall_end):
				if is_horizontal:
					if pos[1] % 2 != 0:
						char_array[pos[0]][pos[1]] = '-'
				else:
					if pos[0] % 2 != 0:
						char_array[pos[0]][pos[1]] = '|'
				pos = pos + diff

		return '\n'.join([''.join(x) for x in char_array])

	def to_single_line_string(self):
		raise ValueError("Not yet implemented")

if __name__ == '__main__':
	board = empty().play('X', ['P', a([7, 4])]).play('O', ['W', a([7, 3]), a([7, 5])])
	print(board)
	print(board.x_route_to_home)
