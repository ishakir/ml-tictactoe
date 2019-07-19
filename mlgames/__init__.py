from mlgames.match import Match

class HashableMoveChoice:
	def __init__(self, board, typ, move):
		self.board = board
		self.typ = typ
		self.move = move

	def __hash__(self):
		h1 = hash(self.board.to_single_line_string())
		h2 = hash(self.typ)
		h3 = hash(str(self.move))

		return hash("".join([str(h) for h in sorted([h1, h2, h3])]))

	def __eq__(self, other):
		return self.board.to_single_line_string() == other.board.to_single_line_string() and \
				self.typ == other.typ and self.move == other.move

	def __str__(self):
		return "{},{},{}".format(self.board.to_single_line_string(), self.typ, str(self.move))


def round_robin_mix(players, empty_board_gen):
	matches = []
	for x in players:
		for o in players:
			matches.append(Match([x, o], empty_board_gen))

	return matches


def all_v_one_mix(players, player, play_first, empty_board_gen):
	matches = []
	for p in players:
		if play_first:
			matches.append(Match([player, p], empty_board_gen))
		else:
			matches.append(Match([p, player], empty_board_gen))

	return matches
