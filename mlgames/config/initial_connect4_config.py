import tensorflow as tf
from tensorflow import keras

from mlgames.config.config_abc import ConfigABC

from mlgames.connect4.board import empty

BOARD_HEIGHT = 6
BOARD_WIDTH = 7

class InitialConnect4Config(ConfigABC):
	def name(self):
		return "initial_connect4"

	def number_of_bots(self):
		return 25

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
		return 10

	def should_train(self):
		def f(results):
			def result_value(result):
				return 5 if result == 'win' else 1 if result == 'draw' else -3
			return sum([result_value(r) for r in results]) / len(results) > 0
		return f

	def benchmark_minimax_depth(self):
		return 2

	def board_evaluation(self):
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

		def evaluate(board, piece):
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

		return evaluate