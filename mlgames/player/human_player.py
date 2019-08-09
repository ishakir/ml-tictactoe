from mlgames.player import Player

class HumanPlayer(Player):
	def name(self):
		return "Human Player"

	def play(self, board, piece):
		while True:
			result = input("What would you like to do?\n").strip()
			try:
				return board.parse_move(result)
			except Exception as e:
				print("Runtime Error parsing move, please try again")

	def new_game(self, result):
		pass

	def new_batch(self, dir):
		pass

	def save(self, dir):
		pass
