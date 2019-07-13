class IfWinPlayer:
	def __init__(self):
		self.name = "If Win Player"
		self.__random = RandomPlayer()

	def play(self, board, type):
		for combination in board.win_combinations:
			vals = map(lambda y: board.value(y[0], y[1]), combination)
			if set(vals) == set(['.', type]) and len([x for x in vals if x == type]) == 2:
				for a, b in combination:
					if board.value(a, b) == '.':
						return a, b
		return self.__random.play(board)

	def new_game(self, result):
		pass

	def new_batch(self):
		pass

	def save(self, dir):
		pass
