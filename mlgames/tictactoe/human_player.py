from mlgames.player import Player

class HumanPlayer(Player):
	def name(self):
		return "Human Player"

	def play(self, board, type):
		result = input("What would you like to do?\n")
		a, b = result.strip().split(",")
		return int(a), int(b)

	def new_game(self, result):
		pass

	def new_batch(self, dir):
		pass

	def save(self, dir):
		pass
