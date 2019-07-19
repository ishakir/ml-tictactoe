from mlgames import round_robin_mix, all_v_one_mix
from mlgames.config.active_config import CURRENT_CONFIG as config
from mlgames.round import Round

from collections import defaultdict
from contextlib import contextmanager
import click
from os import makedirs, path
import sys
from time import time

@contextmanager
def timing(log_statement):
	before = time()
	yield
	after = time()
	print("{} took {:.0f} seconds".format(log_statement, after - before))

@click.command()
@click.option('--resume-from-round', default=0)
@click.option('--data-root', default='.')
def run(resume_from_round, data_root):
	# This is what we change
	config_dir = path.join(data_root, config.name())

	if resume_from_round == 0:
		players = [config.new_machine_learning_player(x) for x in range(config.number_of_bots())]
	else:
		players = [config.load_machine_learning_player(config_dir, resume_from_round, x) for x in range(config.number_of_bots())]

	benchmark_play_first = config.new_benchmark_player(True)
	benchmark_play_second = config.new_benchmark_player(False)

	for i in range(resume_from_round, 100000):
		print('ROUND {}'.format(str(i)))

		round_dir = path.join(config_dir, str(i))
		players_dir = path.join(round_dir, 'starting_players')
		training_dir = path.join(round_dir, 'training_log')
		round_robin_results_dir = path.join(round_dir, 'round_robin')
		benchmark_result_dir = path.join(round_dir, 'benchmark')
		
		makedirs(players_dir, exist_ok=True)
		makedirs(round_robin_results_dir, exist_ok=True)
		makedirs(benchmark_result_dir, exist_ok=True)
		makedirs(training_dir, exist_ok=True)

		with timing('- Saving players'):
			for player in players:
				player.save(players_dir)
		
		with timing('- Playing Matches'):
			round = Round(round_robin_mix(players, config.empty_board_gen()))
			round.play_all()

		with timing('- Saving Round'):
			round.save(round_robin_results_dir)

		with timing('- Comparing against benchmark'):
			for player in players:
				player.training_mode = False
			minimax_round = Round(all_v_one_mix(players, benchmark_play_first, True, config.empty_board_gen()) + all_v_one_mix(players, benchmark_play_second, False, config.empty_board_gen()))
			minimax_round.play_all()
			minimax_round.save(benchmark_result_dir)
			for player in players:
				player.training_mode = True

		with timing('- Training'.format(i)):
			for x in players:
				x.new_batch(training_dir)

		sys.stdout.flush()


if __name__ == '__main__':
	run()
