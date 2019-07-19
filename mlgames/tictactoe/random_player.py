from mlgames.player import Player
from random import randint

class RandomPlayer(Player):
	def name(self):
		return "Random Player"

	def play(self, board, piece):
		while True:
			x, y = randint(0, 2), randint(0, 2)
			if board.play_is_legal(piece, (x, y)):
				return x, y
	
	def new_game(self, result):
		pass

	def new_batch(self, dir):
		pass

	def save(self, dir):
		pass
