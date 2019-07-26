from os import path

class Round:
	def __init__(self, matches):
		self.matches = matches

	def play_all(self, print_progress=True):
		for index, match in enumerate(self.matches):
			if index != 0 and index % 500 == 0 and print_progress:
				print("Ran {} / {} matches".format(index, len(self.matches)))
			
			match.play_until_finished()
			
			res = match.winner()
			match.players[0].new_game('win' if res == 'X' else 'draw' if res is None else 'loss')
			match.players[1].new_game('win' if res == 'O' else 'draw' if res is None else 'loss')

	def summary(self):
		results = []
		for match in self.matches:
			summary = match.summary()
			results.append({
				'X': summary['X'].name(), 
				'O': summary['O'].name(), 
				'winner': summary['winner'],
				'game_length': summary['game_length']
			})
		return results

	def save(self, dir):
		for match in self.matches:
			match_fname = path.join(dir, "{} v {}.txt".format(match.players[0].name(), match.players[1].name()))
			match.save(match_fname)

		with open(path.join(dir, 'results_summary.csv'), 'w') as f:
			f.write(",".join(['X', 'O', 'result', 'game_length']))
			f.write("\n")
			for match in self.matches:
				summary = match.summary()
				f.write(",".join([summary['X'].name(), summary['O'].name(), summary['winner'] if summary['winner'] else 'draw', str(summary['game_length'])]))
				f.write("\n")
