class HumanPlayer:
	def __init__(self):
		self.name = "Human Player"

	def play(self, board, type):
		result = input("What would you like to do?\n")
		a, b = result.strip().split(",")
		return int(a), int(b)

	def new_game(self, result):
		pass

	def new_batch(self):
		pass

	def save(self, dir):
		pass
