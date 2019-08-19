from mlgames.config.config_abc import ConfigABC
from mlgames.quoridor.board import empty as lame
from mlgames.quoridor.networkx_board import empty

import networkx as nx

class InitialQuoridorConfig(ConfigABC):
	def name(self):
		return 'Initial Quoridor'

	def number_of_bots(self):
		return 25

	def empty_board_gen(self):
		return empty

	def new_model(self):
		raise ValueError('Not yet implemented')
	
	def board_to_input(self):
		raise ValueError('Not yet implemented')
	
	def move_to_prediction(self):
		raise ValueError('Not yet implemented')
	
	def prediction_to_move(self):
		raise ValueError('Not yet implemented')

	def epochs(self):
		return 5

	def good_move_confidence_appearance_threshold(self):
		return 1

	def should_train(self):
		def f(results):
			return 'win' in results or 'draw' in results
		return f

	def benchmark_minimax_depth(self):
		return 4

	def board_evaluation(self):
		def evaluate(board, piece):
			x_shortest_path = nx.shortest_path_length(board.graph, str(board.x_position), 'top')
			o_shortest_path = nx.shortest_path_length(board.graph, str(board.o_position), 'bottom')

			print("X shortest: " + str(x_shortest_path))
			print("O shortest: " + str(o_shortest_path))

			if piece == 'X':
				return o_shortest_path - x_shortest_path
			elif piece == 'O':
				return x_shortest_path - o_shortest_path
			else:
				raise ValueError('Not sure what this piece is: {}'.format(piece))
		return evaluate
