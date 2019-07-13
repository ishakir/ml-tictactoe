from tictactoe799.match import Match

NUMBER_OF_BOTS = 25

GOOD_MOVE_CONFIDENCE_APPEARANCE_THRESHOLD = 10

class HashableArray(object):
	def __init__(self, val):
		self.val = val

	def __hash__(self):
		return hash(str(self.val))

	def __repr__(self):
		# Bonus: define this method to get clean output
		return str(self.val)

	def __eq__(self, other):
		return str(self.val) == str(other.val)


def round_robin_mix(players):
	matches = []
	for x in players:
		for o in players:
			matches.append(Match([x, o]))

	return matches


def all_v_one_mix(players, player, play_first):
	matches = []
	for p in players:
		if play_first:
			matches.append(Match([player, p]))
		else:
			matches.append(Match([p, player]))

	return matches