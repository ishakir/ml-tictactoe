import csv

PIECES = ['X', 'O']

class Match:
	def __init__(self, players, empty_board_gen):
		self.players = players
		self.previous_boards = []
		self.current_board = empty_board_gen()
		self.player_index = 1

	def play_next(self):
		if not self.is_finished():
			self.player_index = (self.player_index + 1) % 2
			p = self.players[self.player_index]
			piece = PIECES[self.player_index]

			move = p.play(self.current_board, piece)
			self.previous_boards.append((self.current_board, piece))
			self.current_board = self.current_board.play(piece, move)


	def play_until_finished(self):
		while not self.is_finished():
			self.play_next()

	def next_to_play(self):
		if self.is_finished():
			return None
		else:
			return PIECES[(self.player_index + 1) % 2]

	def is_finished(self):
		return self.current_board.winner() or self.current_board.complete()

	def winner(self):
		return self.current_board.winner()

	def summary(self):
		return {
			'X': self.players[0],
			'O': self.players[1],
			'winner': self.winner(),
			'game_length': len(self.previous_boards) + 1
		}

	def save(self, file):
		with open(file, 'w') as f:
			f.write("{} (X) v {} (O)\n\n".format(self.players[0].name(), self.players[1].name()))
			for board in self.previous_boards:
				f.write("{}\n\n".format(str(board[0])))
			f.write(str(self.current_board))
