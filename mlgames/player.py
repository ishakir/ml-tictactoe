from abc import ABC, abstractmethod

class Player:
	@abstractmethod
	def name(self):
		pass

	@abstractmethod
	def play(self, board, type):
		pass

	@abstractmethod
	def new_game(self, result):
		pass

	@abstractmethod
	def new_batch(self, dir):
		pass

	@abstractmethod
	def save(self, dir):
		pass
