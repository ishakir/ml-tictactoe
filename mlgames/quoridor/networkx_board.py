from mlgames.board import Board

import networkx as nx
import numpy as np

BOARD_SIZE = 9
STARTING_WALLS = 10

def a(arr):
	return np.array(arr)

def empty():
	g = nx.DiGraph()

	g.add_node('top')
	g.add_node('bottom')

	# Add all of the board positions 
	for x in range(BOARD_SIZE):
		for y in range(BOARD_SIZE):
			g.add_node(str(a([x, y])))

	# Add edges to the final nodes
	for x in range(BOARD_SIZE):
		g.add_edge(str(a([0, x])), 'top')
		g.add_edge(str(a([8, x])), 'bottom')

	# Add connections between all of the places on the board
	for x in range(BOARD_SIZE):
		for y in range(BOARD_SIZE):
			position = a([x, y])
			north = position + a([0, -1])
			east = position + a([1, 0])
			south = position + a([0, 1])
			west = position + a([-1, 0])

			str_pos = str(position)
			str_north, str_east, str_south, str_west = str(north), str(east), str(south), str(west)

			if g.has_node(str_north):
				g.add_edge(str_pos, str_north)
			if g.has_node(str_east):
				g.add_edge(str_pos, str_east)
			if g.has_node(str_south):
				g.add_edge(str_pos, str_south)
			if g.has_node(str_west):
				g.add_edge(str_pos, str_west)

	# Account for the player starting positions
	x_starting_position = a([8, 4])
	x_east = x_starting_position + a([0, 1])
	x_north = x_starting_position + a([-1, 0])
	x_west = x_starting_position + a([0, -1])

	str_x_pos = str(x_starting_position)
	str_x_east, str_x_north, str_x_west = str(x_east), str(x_north), str(x_west)

	if g.has_node(str_x_east):
		g.remove_edge(str_x_east, str_x_pos)
		g.add_edge(str_x_north, str_x_east)
	if g.has_node(str_x_west):
		g.remove_edge(str_x_west, str_x_pos)
		g.add_edge(str_x_north, str_x_west)
	if g.has_node(str_x_east) and g.has_node(str_x_west):
		g.add_edge(str_x_east, str_x_west)
		g.add_edge(str_x_west, str_x_east)
	g.remove_edge(str_x_north, str_x_pos)

	o_starting_position = a([0, 4])
	o_east = o_starting_position + a([0, 1])
	o_south = o_starting_position + a([1, 0])
	o_west = o_starting_position + a([0, -1])

	str_o_pos = str(o_starting_position)
	str_o_east, str_o_south, str_o_west = str(o_east), str(o_south), str(o_west)

	if g.has_node(str_o_east):
		g.remove_edge(str_o_east, str_o_pos)
		g.add_edge(str_o_south, str_o_east)
	if g.has_node(str_o_west):
		g.remove_edge(str_o_west, str_o_pos)
		g.add_edge(str_o_south, str_o_west)
	if g.has_node(str_o_west) and g.has_node(str_o_east):
		g.add_edge(str_o_east, str_o_west)
		g.add_edge(str_o_west, str_o_east)
	g.remove_edge(str_o_south, str_o_pos)

	print(g.edges('[1 4]'))
	
	return NetworkXQuoridorBoard(g, x_starting_position, o_starting_position)


# TODO: Have not taken account of walls at all in move methods
class NetworkXQuoridorBoard(Board):
	def __init__(self, graph, x_position, o_position):
		self.graph = graph
		self.x_position = x_position
		self.o_position = o_position

	# Maybe can do this more neatly with graph.edges(), but not entirely sure
	def resolve_move(self, current_pos, direction):
		str_current_pos = str(current_pos)

		possible_moves = []
		if direction == 'N':
			possible_moves.append(a([-1, 0]))
			possible_moves.append(a([-2, 0]))
		elif direction == 'S':
			possible_moves.append(a([1, 0]))
			possible_moves.append(a([2, 0]))
		elif direction == 'E':
			possible_moves.append(a([0, 1]))
			possible_moves.append(a([0, 1]))
		elif direction == 'W':
			possible_moves.append(a([0, -1]))
			possible_moves.append(a([0, -2]))
		elif direction == 'NE':
			possible_moves.append(a([-1, 1]))
		elif direction == 'SE':
			possible_moves.append(a([1, 1]))
		elif direction == 'SW':
			possible_moves.append(a([1, -1]))
		elif direction == 'NW':
			possible_moves.append(a([-1, -1]))
		else:
			raise ValueError("Don't recognize direction {}".format(direction))

		for move in possible_moves:
			to = current_pos + move
			str_to = str(to)
			if self.graph.has_node(str_to) and self.graph.has_edge(str_current_pos, str_to):
				return to
		return None


	def play(self, piece, move):
		g = self.graph.copy()
		source = self.x_position if piece == 'X' else self.o_position
		str_current_pos = str(source)

		move_type = move[0]
		if move_type == 'P':
			direction = move[1]
			target = self.resolve_move(source, direction)
			str_target = str(target)

			s_north, s_east, s_south, s_west = source + a([-1, 0]), source + a([0, 1]), source + a([1, 0]), source + a([0, -1])
			t_north, t_east, t_south, t_west = target + a([-1, 0]), target + a([0, 1]), target + a([1, 0]), target + a([0, -1])

			str_s_north, str_s_east, str_s_south, str_s_west = str(s_north), str(s_east), str(s_south), str(s_west)
			str_t_north, str_t_east, str_t_south, str_t_west = str(t_north), str(t_east), str(t_south), str(t_west)

			if g.has_node(str_s_north):
				if g.has_node(str_s_south):
					g.remove_edge(str_s_north, str_s_south)
				else:
					if g.has_node(str_s_east):
						g.remove_edge(str_s_north, str_s_east)
					if g.has_node(str_s_west):
						g.remove_edge(str_s_north, str_s_west)
				g.add_edge(str_s_north, str_current_pos)
			if  g.has_node(str_s_south):
				if g.has_node(str_s_north):
					g.remove_edge(str_s_south, str_s_north)
				else:
					if g.has_node(str_s_east):
						g.remove_edge(str_s_south, str_s_east)
					if g.has_node(str_s_west):
						g.remove_edge(str_s_south, str_s_west)
				g.add_edge(str_s_south, str_current_pos)
			if g.has_node(str_s_east):
				if g.has_node(str_s_west):
					g.remove_edge(str_s_east, str_s_west)
				else:
					if g.has_node(str_s_north):
						g.remove_edge(str_s_east, str_s_north)
					if g.has_node(str_s_south):
						g.remove_edge(str_s_east, str_s_south)
				g.add_edge(str_s_east, str_current_pos)
			if g.has_node(str_s_west):
				if g.has_node(str_s_east):
					g.remove_edge(str_s_west, str_s_east)
				else:
					if g.has_node(str_s_north):
						g.remove_edge(str_s_west, str_s_north)
					if g.has_node(str_s_south):
						g.remove_edge(str_s_west, str_s_south)
				g.add_edge(str_s_west, str_current_pos)

			if g.has_node(str_t_north):
				g.remove_edge(str_t_north, str_target)
				if g.has_node(str_t_south):
					g.add_edge(str_t_north, str_t_south)
				else:
					if g.has_node(str_t_east):
						g.add_edge(str_t_north, str_t_east)
					if g.has_node(str_t_west):
						g.add_edge(str_t_north, str_t_west)
			if g.has_node(str_t_south):
				g.remove_edge(str_t_south, str_target)
				if g.has_node(str_t_north):
					g.add_edge(str_t_south, str_t_north)
				else:
					if g.has_node(str_t_east):
						g.add_edge(str_t_south, str_t_east)
					if g.has_node(str_t_west):
						g.add_edge(str_t_south, str_t_west)
			if g.has_node(str_t_east):
				g.remove_edge(str_t_east, str_target)
				if g.has_node(str_t_west):
					g.add_edge(str_t_east, str_t_west)
				else:
					if g.has_node(str_t_north):
						g.add_edge(str_t_east, str_t_north)
					if g.has_node(str_t_south):
						g.add_edge(str_t_east, str_t_south)
			if  g.has_node(str_t_west):
				g.remove_edge(str_t_west, str_target)
				if g.has_node(str_t_east):
					g.add_edge(str_t_west, str_t_east)
				else:
					if g.has_node(str_t_north):
						g.add_edge(str_t_west, str_t_north)
					if g.has_node(str_t_south):
						g.add_edge(str_t_west, str_t_south)

			if piece == 'X':
				return NetworkXQuoridorBoard(g, target, self.o_position)
			elif piece == 'O':
				return NetworkXQuoridorBoard(g, self.x_position, target)
			else:
				raise ValueError("Don't recognize piece {}".format(piece))


	def winner(self):
		if self.x_position[0] == 0:
			return 'X'
		elif self.o_position[0] == 8:
			return 'O'
		else:
			return None

	def parse_move(self, move_str):
		split = move_str.split()
		if split[0] == 'P':
			return split

	def play_is_legal(self, piece, move):
		current_pos = self.x_position if piece == 'X' else self.o_position
		str_current_pos = str(current_pos)

		move_type = move[0]
		if move_type == 'P':
			direction = move[1]
			return self.resolve_move(current_pos, direction) is not None


	def all_legal_moves(self, piece):
		all_moves = [
			['P', 'N'],
			['P', 'S'],
			['P', 'E'],
			['P', 'W'],
			['P', 'NE'],
			['P', 'SE'],
			['P', 'SW'],
			['P', 'NW']
		]

		return [m for m in all_moves if self.play_is_legal(piece, m)]

	# Game is never a draw, winner() should return when someone wins
	def complete(self):
		return False

	def all_symmetries(self, move):
		pass

	# In short, the algorithm is this:
	# If the 'target' square does not have an opponent, then it's enough that you can move into it
	# If the 'target' square does have an opponent, then you have only proved that either the opponent
	# can be jumped (in at least one direction) from the square you are considering OR the opponent can
	# jump the square you are in in at least one direction
	def has_wall_to_north(self, center):
		str_center = str(center)
		north, south, east, west = center + a([-1, 0]), center + a([1, 0]), center + a([0, 1]), center + a([0, -1])
		str_north, str_south, str_east, str_west = str(north), str(south), str(east), str(west)

		further_north, north_east, north_west = center + a([-2, 0]), center + a([-1, 1]), center + a([-1, -1])
		str_further_north, str_north_east, str_north_west = str(further_north), str(north_east), str(north_west)

		north_is_reachable = self.graph.has_node(str_north) and self.graph.has_edge(str_center, str_north)
		further_north_is_reachable = self.graph.has_node(str_further_north) and self.graph.has_edge(str_center, str_further_north)
		north_east_is_reachable = self.graph.has_node(str_north_east) and self.graph.has_edge(str_center, str_north_east)
		north_west_is_reachable = self.graph.has_node(str_north_west) and self.graph.has_edge(str_center, str_north_west)

		wall_is_reachable = self.graph.has_node(str_center) and self.graph.has_edge(str_north, str_center)
		south_is_reachable = self.graph.has_node(str_south) and self.graph.has_edge(str_north, str_south)
		east_is_reachable = self.graph.has_node(str_east) and self.graph.has_edge(str_north, str_east)
		west_is_reachable = self.graph.has_node(str_west) and self.graph.has_edge(str_north, str_west)

		if not self.graph.has_node(str_north):
			return False 
		return not north_is_reachable and not further_north_is_reachable and not north_east_is_reachable and not north_west_is_reachable and not wall_is_reachable and not south_is_reachable and not east_is_reachable and not west_is_reachable


	def has_wall_to_west(self, center):
		str_center = str(center)
		north, south, east, west = center + a([-1, 0]), center + a([1, 0]), center + a([0, 1]), center + a([0, -1])
		str_north, str_south, str_east, str_west = str(north), str(south), str(east), str(west)

		further_west, south_west, north_west = center + a([0, -2]), center + a([1, -1]), center + a([-1, -1])
		str_further_west, str_south_west, str_north_west = str(further_west), str(south_west), str(north_west)

		west_is_reachable = self.graph.has_node(str_west) and self.graph.has_edge(str_center, str_west)
		further_west_is_reachable = self.graph.has_node(str_further_west) and self.graph.has_edge(str_center, str_further_west)
		south_west_is_reachable = self.graph.has_node(str_south_west) and self.graph.has_edge(str_center, str_south_west)
		north_west_is_reachable = self.graph.has_node(str_north_west) and self.graph.has_edge(str_center, str_north_west)

		wall_is_reachable = self.graph.has_node(str_center) and self.graph.has_edge(str_west, str_center)
		south_is_reachable = self.graph.has_node(str_south) and self.graph.has_edge(str_west, str_south)
		east_is_reachable = self.graph.has_node(str_east) and self.graph.has_edge(str_west, str_east)
		north_is_reachable = self.graph.has_node(str_north) and self.graph.has_edge(str_west, str_north)

		if not self.graph.has_node(str_west):
			return False
		return not west_is_reachable and not further_west_is_reachable and not south_west_is_reachable and not north_west_is_reachable and not wall_is_reachable and not south_is_reachable and not east_is_reachable and not north_is_reachable

	def has_wall_to_south(self, center):
		return has_wall_to_north(center + [0, 1])

	def has_wall_to_east():
		return has_wall_to_west(center + [1, 0])

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

		for x in range(0, BOARD_SIZE):
			for y in range(0, BOARD_SIZE):
				wall = a([x, y])
				str_wall = str(wall)

				if self.has_wall_to_north(wall):
					board_coord = (wall * 2) + a([0, 1])
					char_array[board_coord[0]][board_coord[1]] = '-'

				if self.has_wall_to_west(wall):
					board_coord = (wall * 2) + a([1, 0])
					char_array[board_coord[0]][board_coord[1]] = '|'

		return '\n'.join([''.join(x) for x in char_array])

	def to_single_line_string(self):
		pass


if __name__ == '__main__':
	board = empty()
	print(board)
