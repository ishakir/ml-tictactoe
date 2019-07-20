from abc import ABC, abstractmethod
from os import path
from tensorflow import keras

from mlgames.machine_learning_player import MachineLearningPlayer

class ConfigABC(ABC):
	@abstractmethod
	def name(self):
		pass

	@abstractmethod
	def number_of_bots(self):
		pass

	@abstractmethod
	def new_human_player(self):
		pass

	@abstractmethod
	def new_random_player(self):
		pass

	def new_machine_learning_player(self, bot_number):
		return MachineLearningPlayer(
			number=bot_number,
			model=self.new_model(),
			random_player=self.new_random_player(),
			move_to_prediction=self.move_to_prediction(),
			prediction_to_move=self.prediction_to_move(),
			board_to_input=self.board_to_input(),
			epochs=self.epochs(),
			good_move_confidence_appearance_threshold=self.good_move_confidence_appearance_threshold(),
			should_train=self.should_train()
		)

	def load_machine_learning_player(self, data_root, round, bot_number):
		saved_model = path.join(data_root, str(round), 'starting_players', '{}.h5'.format(str(bot_number)))
		return MachineLearningPlayer(
			number=bot_number,
			model=keras.models.load_model(saved_model),
			random_player=self.new_random_player(),
			move_to_prediction=self.move_to_prediction(),
			prediction_to_move=self.prediction_to_move(),
			board_to_input=self.board_to_input(),
			epochs=self.epochs(),
			good_move_confidence_appearance_threshold=self.good_move_confidence_appearance_threshold(),
			should_train=self.should_train()
		)

	@abstractmethod
	def new_benchmark_player(self, play_first):
		pass

	@abstractmethod
	def empty_board_gen(self):
		pass

	@abstractmethod
	def new_model(self):
		pass

	@abstractmethod	
	def board_to_input(self):
		pass

	@abstractmethod	
	def move_to_prediction(self):
		pass

	@abstractmethod	
	def prediction_to_move(self):
		pass

	@abstractmethod
	def epochs(self):
		pass

	@abstractmethod
	def good_move_confidence_appearance_threshold(self):
		pass

	@abstractmethod
	def should_train(self):
		pass
