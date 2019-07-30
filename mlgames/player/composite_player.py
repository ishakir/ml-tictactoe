from mlgames.player import Player

import random

class CompositePlayer(Player):
	def __init__(self, primary, secondary, primaryness):
		self.primary = primary
		self.secondary = secondary
		self.primaryness = primaryness

	def name(self):
		return "({:.2f}%) {} + ({:.2f}%) {}".format(self.primaryness * 100, self.primary.name(), (1 - self.primaryness) * 100, self.secondary.name())

	def play(self, board, piece):
		if random.uniform(0, 1) < self.primaryness:
			return self.primary.play(board, piece)
		else:
			return self.secondary.play(board, piece)

	def new_game(self, result):
		pass

	def new_batch(self, dir):
		pass

	def save(self, dir):
		pass
