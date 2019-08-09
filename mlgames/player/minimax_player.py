from random import shuffle

from mlgames.player import Player

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
	def __init__(self, termination_depth, board_to_score):
		self.termination_depth = termination_depth
		self.board_to_score = board_to_score

	def name(self):
		return "Minimax Player"

	def play(self, board, piece):
		positions_to_score = []
		stack = []
		total_nodes = 0

		moves = board.all_legal_moves(piece)
		shuffle(moves)
		for x in moves:
			new_node = Node(board.play(piece, x), None, 1, False, None)
			positions_to_score.append((x, new_node))
			stack.append(new_node)
			total_nodes += 1

		while not len(stack) == 0:
			node = stack.pop(0)
			total_nodes += 1
			if node.depth == self.termination_depth:
				node.total_children = 1
				node.report_result(self.board_to_score(node.board, piece))
			else:
				if node.depth % 2 == 0:
					piece_to_play = piece
				else:
					piece_to_play = 'O' if piece == 'X' else 'X'

				moves = node.board.all_legal_moves(piece_to_play)
				shuffle(moves)
				for x in moves:
					node.total_children = len(moves)
					stack.append(Node(node.board.play(piece_to_play, x), node, node.depth + 1, not node.us_to_play, None))
					total_nodes += 1

		best = None
		best_score = -1

		for play, node in positions_to_score:
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
