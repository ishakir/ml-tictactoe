from mlgames.player import Player
from random import choice

class RandomPlayer:
	def name(self):
		return "Random Player"

	def play(self, board, piece):
		return choice(board.all_legal_moves(piece))

	def new_game(self, result):
		pass

	def new_batch(self, dir):
		pass

	def save(self, dir):
		pass
