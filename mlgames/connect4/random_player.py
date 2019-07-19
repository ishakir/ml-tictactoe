from mlgames.player import Player
from random import randint

class RandomPlayer:
	def name(self):
		return "Random Player"

	def play(self, board, piece):
		while True:
			col = randint(0, 6)
			if board.play_is_legal(piece, col):
				return col

	def new_game(self, result):
		pass

	def new_batch(self, dir):
		pass

	def save(self, dir):
		pass
