import csv

from tictactoe799.board import Board

TYPES = ['X', 'O']

class Match:
	def __init__(self, players):
		self.players = players
		self.previous_boards = []
		self.current_board = Board([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']])
		self.player_index = 1

	def play_next(self):
		if not self.is_finished():
			self.player_index = (self.player_index + 1) % 2
			p = self.players[self.player_index]
			type = TYPES[self.player_index]

			x, y = p.play(self.current_board, type)
			self.previous_boards.append((self.current_board, type))
			self.current_board = self.current_board.place(type, x, y)


	def play_until_finished(self):
		while not self.is_finished():
			self.play_next()

	def next_to_play(self):
		if self.is_finished():
			return None
		else:
			return TYPES[(self.player_index + 1) % 2]

	def is_finished(self):
		return self.current_board.winner() or self.current_board.full()

	def winner(self):
		return self.current_board.winner()

	def summary(self):
		return {
			'X': self.players[0],
			'O': self.players[1],
			'winner': self.winner()
		}

	def save(self, file):
		with open(file, 'w') as f:
			f.write("{} (X) v {} (O)\n\n".format(self.players[0].name, self.players[1].name))
			for board in self.previous_boards:
				f.write("{}\n\n".format(str(board[0])))
			f.write(str(self.current_board))
