from tictactoe799 import HashableMoveChoice, GOOD_MOVE_CONFIDENCE_APPEARANCE_THRESHOLD
from tictactoe799.player.random_player import RandomPlayer

from collections import defaultdict
from random import randint
import tensorflow as tf
from tensorflow import keras
import numpy as np

from os import path


def load_model(round, number):
	saved_model = path.join('.', 'output', str(round), 'starting_players', '{}.h5'.format(str(number)))
	return MachineLearningPlayer(number, keras.models.load_model(saved_model))


class MachineLearningPlayer:
	def __init__(self, number, model=None):
		self.name = "ML Bot {}".format(number)
		self.number = number
		self.random = RandomPlayer()
		self.training_mode = True

		if model is None:
			self.model = keras.Sequential([
			    keras.layers.Dense(64, activation=tf.nn.relu, input_shape=(27, )),
			    keras.layers.Dense(16, activation=tf.nn.relu),
			    keras.layers.Dense(9, activation=tf.nn.softmax)
			])

			self.model.compile(optimizer='adam',
	             loss='sparse_categorical_crossentropy',
	             metrics=['accuracy'])
		else:
			self.model = model

		self.training_data = defaultdict(list)
		self.staged_training_data = []

	def board_to_binary_state(self, board, type):
		def translate(val):
			return [True, False, False] if val == type else [False, True, False] if not val == '.' else [False, False, True]
		binary_state = []
		for b in board.board_state:
			for a in b:
				binary_state.extend(translate(a))
		return binary_state

	def p_2_index(self, position):
		return (position[0] * 3) + position[1]

	def add_training_data(self, board, typ, x, y):
		if self.training_mode:
			self.staged_training_data.append(HashableMoveChoice(board, typ, [x, y]))
			self.staged_training_data.append(HashableMoveChoice(board.reflect_board_x(), typ, board.reflect_position_x([x, y])))
			self.staged_training_data.append(HashableMoveChoice(board.reflect_board_y(), typ, board.reflect_position_y([x, y])))
			self.staged_training_data.append(HashableMoveChoice(board.rotate_board(1), typ, board.rotate_position([x, y], 1)))
			self.staged_training_data.append(HashableMoveChoice(board.rotate_board(2), typ, board.rotate_position([x, y], 2)))
			self.staged_training_data.append(HashableMoveChoice(board.rotate_board(3), typ, board.rotate_position([x, y], 3)))

	def play(self, board, type):
		if self.training_mode and randint(0, 9) == 0:
			first, second = self.random.play(board, type)
			self.add_training_data(board, type, first, second)	
			return first, second
		else:
			prediction = self.model.predict(np.array([self.board_to_binary_state(board, type)]))
			
			for index, x in sorted(enumerate(prediction[0]), key=lambda x: -x[1]):
				remainder = index % 3
				quotient = int((index - remainder) / 3)
				if not board.taken(quotient, remainder):
					self.add_training_data(board, type, quotient, remainder)
					return quotient, remainder
		raise RuntimeError("Failed to find any")

	def new_game(self, result):
		for move_choice in self.staged_training_data:
			self.training_data[move_choice].append(result)
		self.staged_training_data = []

	def __result_value(self, result):
		return 5 if result == 'win' else 1 if result == 'draw' else -3

	def new_batch(self, dir):
		above_threshold = {k: v for k, v in self.training_data.items() if len(v) > GOOD_MOVE_CONFIDENCE_APPEARANCE_THRESHOLD}
		to_train = [k for k, v in above_threshold.items() if sum([self.__result_value(r) for r in v]) / len(v) > 0]

		with open(path.join(dir, "{}_training.csv".format(str(self.number))), 'w') as f:
			f.write("board,to_play,move_x,move_y\n")
			for x in to_train:
				f.write("{}\n".format(str(x)))

		for k, _ in above_threshold.items():
			del self.training_data[k]

		if to_train:
			self.model.fit(
				np.array([self.board_to_binary_state(x.board, x.typ) for x in to_train]),
				np.array([self.p_2_index(y.move) for y in to_train]),
				epochs=5,
				verbose=0
			)

	def save(self, dir):
		self.model.save(path.join(dir, '{}.h5'.format(str(self.number))))
