from mlgames.player import Player

import csv
import random

class MinimaxPlayer(Player):
	def __init__(self, play_first):
		self.play_first = play_first

		self.board_states = {}

		with open('tictactoe_minimax_state.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				self.board_states[row['board_state']] = int(row['result'])

	def name(self):
		return "Minimax Player"

	def play(self, board, piece):
		possible_moves = []
		for x in range(3):
			for y in range(3):
				if board.play_is_legal(piece, (x, y)):
					possible_moves.append((x, y))

		ones = []
		zeros = []
		minus_ones = []

		for x, y in possible_moves:
			new_board = board.play(piece, [x, y])
			score = self.board_states[new_board.to_single_line_string()]
			score = score if self.play_first else -1 * score
			if score == 1:
				ones.append((x, y))
			elif score == 0:
				zeros.append((x, y))
			else:
				minus_ones.append((x, y))

		if ones:
			return random.choice(ones)
		elif zeros:
			return random.choice(zeros)
		else:
			return random.choice(minus_ones)

	def new_game(self, result):
		pass

	def new_batch(self, dir):
		pass

	def save(self, dir):
		pass
