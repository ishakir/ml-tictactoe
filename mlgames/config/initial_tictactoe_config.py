import tensorflow as tf
from tensorflow import keras

from mlgames.config.config_abc import ConfigABC

from mlgames.tictactoe.board import empty
from mlgames.tictactoe.minimax_player import MinimaxPlayer

class InitialTicTacToeConfig(ConfigABC):
	def name(self):
		return "tictactoe_learnanywinner"

	def number_of_bots(self):
		return 25

	def new_benchmark_player(self, play_first):
		return MinimaxPlayer(play_first)

	def empty_board_gen(self):
		return empty

	def new_model(self):
		model = keras.Sequential([
		    keras.layers.Dense(64, activation=tf.nn.relu, input_shape=(27, )),
		    keras.layers.Dense(16, activation=tf.nn.relu),
		    keras.layers.Dense(9, activation=tf.nn.softmax)
		])

		model.compile(optimizer='adam',
             loss='sparse_categorical_crossentropy',
             metrics=['accuracy'])

		return model

	def board_to_input(self):
		def f(board, piece):
			def translate(val):
				return [True, False, False] if val == piece else [False, True, False] if not val == b'.' else [False, False, True]
			binary_state = []
			for b in board.board_state:
				for a in b:
					binary_state.extend(translate(a))
			return binary_state
		return f

	def move_to_prediction(self):
		def f(move):
			return (move[0] * 3) + move[1]
		return f

	def prediction_to_move(self):
		def f(prediction):
			remainder = prediction % 3
			quotient = int((prediction - remainder) / 3)
			return quotient, remainder
		return f

	def epochs(self):
		return 5

	def good_move_confidence_appearance_threshold(self):
		return 10

	def should_train(self):
		def f(results):
			def result_value(result):
				return 5 if result == 'win' else 1 if result == 'draw' else -3
			return sum([result_value(r) for r in results]) / len(results) > 0
		return f

	def benchmark_minimax_depth(self):
		raise NotImplemented('new_benchmark_player should be overriden!')

	def board_evaluation(self):
		raise NotImplemented('new_benchmark_player should be overriden!')
