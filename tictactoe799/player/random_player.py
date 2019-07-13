from random import randint

class RandomPlayer:
	def __init__(self):
		self.name = "Random Player"

	def play(self, board, type):
		while True:
			x, y = randint(0, 2), randint(0, 2)
			if not board.taken(x, y):
				return x, y

	def new_game(self, result):
		pass

	def new_batch(self):
		pass

	def save(self, dir):
		pass
