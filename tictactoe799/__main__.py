from tictactoe799 import NUMBER_OF_BOTS, round_robin_mix, all_v_one_mix
from tictactoe799.round import Round
from tictactoe799.player.machine_learning_player import MachineLearningPlayer, load_model
from tictactoe799.player.minimax_player import MinimaxPlayer

from collections import defaultdict
import click

from os import makedirs, path

@click.command()
@click.option('--resume-from-round', default=0)
@click.option('--data-root', default='.')
def run(resume_from_round, data_root):
	if resume_from_round == 0:
		players = [MachineLearningPlayer(x) for x in range(NUMBER_OF_BOTS)]
	else:
		players = [load_model(resume_from_round, x) for x in range(NUMBER_OF_BOTS)]

	minimax_play_first = MinimaxPlayer(True)
	minimax_play_second = MinimaxPlayer(False)

	for i in range(resume_from_round, 10000):
		print('ROUND {}'.format(str(i)))

		round_dir = path.join(data_root, 'output', str(i))
		players_dir = path.join(round_dir, 'starting_players')
		round_robin_results_dir = path.join(round_dir, 'round_robin')
		minimax_result_dir = path.join(round_dir, 'minimax')
		
		makedirs(players_dir, exist_ok=True)
		makedirs(round_robin_results_dir, exist_ok=True)
		makedirs(minimax_result_dir, exist_ok=True)

		print('- Saving players')
		for player in players:
			player.save(players_dir)
		
		print('- Playing Matches')
		round = Round(round_robin_mix(players))
		round.play_all()

		print('- Saving Round')
		round.save(round_robin_results_dir)

		print('- Playing and saving results against minimax player')
		for player in players:
			player.training_mode = False
		minimax_round = Round(all_v_one_mix(players, minimax_play_first, True) + all_v_one_mix(players, minimax_play_second, False))
		minimax_round.play_all()
		minimax_round.save(minimax_result_dir)
		for player in players:
			player.training_mode = True

		print('- Training'.format(i))
		for x in players:
			x.new_batch()


if __name__ == '__main__':
	run()
