import tensorflow as tf
from tensorflow import keras

from mlgames.config.config_abc import ConfigABC
from mlgames.machine_learning_player import MachineLearningPlayer

from mlgames.connect4.board import empty
from mlgames.connect4.human_player import HumanPlayer
from mlgames.connect4.random_player import RandomPlayer
from mlgames.connect4.minimax_player import MinimaxPlayer

class Connect4LearnAnyNonLosingConfig(ConfigABC):
	def name(self):
		return "connect4_learnanynonlosing"

	def number_of_bots(self):
		return 25

	def new_human_player(self):
		return HumanPlayer()

	def new_random_player(self):
		return RandomPlayer()

	def new_benchmark_player(self, play_first):
		return MinimaxPlayer(2)

	def empty_board_gen(self):
		return empty

	def new_model(self):
		model = keras.Sequential([
		    keras.layers.Dense(80, activation=tf.nn.relu, input_shape=(126, )),
		    keras.layers.Dense(35, activation=tf.nn.relu),
		    keras.layers.Dense(7, activation=tf.nn.softmax)
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
		def identity(x):
			return x
		return identity

	def prediction_to_move(self):
		def identity(x):
			return x
		return identity

	def epochs(self):
		return 5

	def good_move_confidence_appearance_threshold(self):
		return 1

	def should_train(self):
		def f(results):
			return 'win' in results or 'draw' in results
		return f
