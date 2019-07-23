from random import shuffle
from collections import defaultdict

from mlgames.player import Player

BOARD_HEIGHT = 6
BOARD_WIDTH = 7

class Node:
	def __init__(self, board, parent, depth, us_to_play, total_children):
		self.board = board
		self.parent = parent
		self.us_to_play = us_to_play
		self.depth = depth
		self.result = None

		self.total_children = total_children
		self.results = []

	def report_result(self, val):
		self.results.append(val)
		if len(self.results) == self.total_children:
			cumulative_result = max(self.results) if self.us_to_play else min(self.results)
			self.result = cumulative_result
			if self.parent:
				self.parent.report_result(cumulative_result)

class MinimaxPlayer(Player):
	def __init__(self, termination_depth):
		self.termination_depth = termination_depth

	def name(self):
		return "Human Player"

	def play(self, board, piece):
		def examine_sublist(sublist):
			values = set(sublist)
			if b'X' in values and b'O' in values:
				return 'not_completable'
			elif b'X' not in values and b'O' not in values in values:
				return 'empty'
			else:
				if b'X' in values:
					return ('X', sublist.count(b'X'))
				else:
					return ('O', sublist.count(b'O'))

		def all_sublists_of_length_four(lst):
			al = []
			for i in range(0, len(lst) - 3):
				al.append(lst[i:i+4].tolist())
			return al


		def board_to_score(board, piece):
			us_completable = defaultdict(lambda: 0)
			them_completable = defaultdict(lambda: 0)
			empty_count = 0
			not_completable_count = 0

			all_groups_of_four = []

			for x in range(BOARD_HEIGHT):
				all_groups_of_four.extend(all_sublists_of_length_four(board.board_state[x, :]))

			for x in range(BOARD_WIDTH):
				all_groups_of_four.extend(all_sublists_of_length_four(board.board_state[:, x]))

			y_reflected = board.reflect_board_y()
			for x in range(-2, 4):
				all_groups_of_four.extend(all_sublists_of_length_four(board.board_state.diagonal(x)))
				all_groups_of_four.extend(all_sublists_of_length_four(y_reflected.board_state.diagonal(x)))

			for group in all_groups_of_four:
				result = examine_sublist(group)
				if result == 'not_completable':
					not_completable_count += 1 
				elif result == 'empty':
					empty_count += 1
				elif result[0] == piece:
					us_completable[result[1]] += 1
				else:
					them_completable[result[1]] += 1

			if us_completable[4] >= 1:
				return 1
			elif them_completable[4] >=1:
				return -1
			if not_completable_count == len(all_groups_of_four):
				return 0
			else:
				return (((100 * (us_completable[3] - them_completable[3])) + (10 * (us_completable[2] - them_completable[2])) + (us_completable[0] - them_completable[0])) / 6900)

		positions_to_score = {}
		stack = []
		total_nodes = 0

		moves = [x for x in range(7)]
		shuffle(moves)
		legal_moves = [x for x in moves if board.play_is_legal(piece, x)]
		for x in legal_moves:
			new_node = Node(board.play(piece, x), None, 1, False, None)
			positions_to_score[x] = new_node
			stack.append(new_node)
			total_nodes += 1

		while not len(stack) == 0:
			node = stack.pop(0)
			total_nodes += 1
			winner = node.board.winner()
			if node.depth == self.termination_depth:
				node.total_children = 1
				node.report_result(board_to_score(node.board, piece))
			else:
				if node.depth % 2 == 0:
					piece_to_play = piece
				else:
					piece_to_play = 'O' if piece == 'X' else 'X'

				moves = [x for x in range(7)]
				shuffle(moves)
				legal_moves = [x for x in moves if node.board.play_is_legal(piece_to_play, x)]
				for x in legal_moves:
					node.total_children = len(legal_moves)
					stack.append(Node(node.board.play(piece_to_play, x), node, node.depth + 1, not node.us_to_play, None))
					total_nodes += 1

		best = None
		best_score = -1

		for play, node in positions_to_score.items():
			if best is None or node.result > best_score:
				best = play
				best_score = node.result

		return best

	def new_game(self, result):
		pass

	def new_batch(self, dir):
		pass

	def save(self, dir):
		pass

if __name__ == '__main__':
	MinimaxPlayer().play(None, None)
