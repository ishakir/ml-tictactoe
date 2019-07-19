from mlgames import HashableMoveChoice

from collections import defaultdict
from random import randint
import tensorflow as tf
from tensorflow import keras
import numpy as np

from os import path


class MachineLearningPlayer:
	def __init__(self, number, model, random_player, move_to_prediction, prediction_to_move, board_to_input, epochs, good_move_confidence_appearance_threshold, should_train):
		self._name = "ML Bot {}".format(number)
		self.number = number
		self.random = random_player
		self.training_mode = True
		self.training_data = defaultdict(list)
		self.staged_training_data = []
		self.good_move_confidence_appearance_threshold = good_move_confidence_appearance_threshold
		self.should_train = should_train
		
		# The model itself
		self.model = model
		self.epochs = epochs

		# This is the translation layer between the board object and the model
		self.board_to_input = board_to_input
		self.move_to_prediction = move_to_prediction
		self.prediction_to_move = prediction_to_move

	def name(self):
		return self._name

	def add_training_data(self, board, piece, move):
		if self.training_mode:
			self.staged_training_data.append(HashableMoveChoice(board, piece, move))
			self.staged_training_data.extend([HashableMoveChoice(board, piece, new_move) for board, new_move in board.all_symmetries(move)])
			

	def play(self, board, piece):
		if self.training_mode and randint(0, 9) == 0:
			move = self.random.play(board, piece)
			self.add_training_data(board, piece, move)	
			return move
		else:
			prediction = self.model.predict(np.array([self.board_to_input(board, piece)]))
			
			for prediction, x in sorted(enumerate(prediction[0]), key=lambda x: -x[1]):
				move = self.prediction_to_move(prediction)
				if board.play_is_legal(piece, move):
					self.add_training_data(board, piece, move)
					return move
		raise RuntimeError("Failed to find any")

	def new_game(self, result):
		for move_choice in self.staged_training_data:
			self.training_data[move_choice].append(result)
		self.staged_training_data = []

	def new_batch(self, dir):
		above_threshold = {k: v for k, v in self.training_data.items() if len(v) >= self.good_move_confidence_appearance_threshold}
		to_train = [k for k, v in above_threshold.items() if self.should_train(v)]

		with open(path.join(dir, "{}_training.csv".format(str(self.number))), 'w') as f:
			f.write("board,to_play,move_x,move_y\n")
			for x in to_train:
				f.write("{}\n".format(str(x)))

		for k, _ in above_threshold.items():
			del self.training_data[k]

		if to_train:
			self.model.fit(
				np.array([self.board_to_input(x.board, x.typ) for x in to_train]),
				np.array([self.move_to_prediction(y.move) for y in to_train]),
				epochs=self.epochs,
				verbose=0
			)

	def save(self, dir):
		self.model.save(path.join(dir, '{}.h5'.format(str(self.number))))
