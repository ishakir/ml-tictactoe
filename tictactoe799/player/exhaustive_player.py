from collections import defaultdict
import csv

class ExhaustivePlayer:
	def __init__(self):
		self.name = "Exhaustive Player"
		self.board_states = {}

		with open('exhaustive_state.csv') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				self.board_states[row[0]] = row[1:]

	def play(self, board, type):
		possible_moves = []
		for x in range(3):
			for y in range(3):
				if not board.taken(x, y):
					possible_moves.append((x, y))

		data_to_consider = []
		for x, y in possible_moves:
			new_board = board.place(type, x, y)
			results = self.board_states[new_board.to_single_line_string()]
			total_children = int(results[0]) + int(results[1]) + int(results[2])
			data_to_consider.append((x, y, float(results[0]) / total_children, float(results[1]) / total_children, float(results[2]) / total_children))

		only_wins = []
		no_losses = []
		minimum_losses = None

		# print("Choosing between the following:")
		for x, y, wins, draws, losses in data_to_consider:
			# print("Play ({},{}) - {:.3f} wins, {:.3f} draws, {:.3f} losses".format(x, y, wins, draws, losses))
			if losses == 0 and draws == 0:
				only_wins.append((x, y))
			elif losses == 0:
				no_losses.append((x, y))
			else:
				if minimum_losses is None:
					minimum_losses = (x, y, losses)
				else:
					_, _, min_losses = minimum_losses
					if losses < min_losses:
						minimum_losses = (x, y, losses)

		if only_wins:
			x, y = only_wins[0]
			return x, y
		elif no_losses:
			x, y = no_losses[0]
			return x, y
		else:
			x, y, _ = minimum_losses
			# print("Choosing {},{}".format(x, y))
			return x, y

	def new_game(self, result):
		pass

	def new_batch(self):
		pass

	def save(self, dir):
		pass
