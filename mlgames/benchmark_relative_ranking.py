from mlgames import all_v_one_mix
from mlgames.composite_player import CompositePlayer
from mlgames.match import Match
from mlgames.round import Round
from mlgames.config.active_config import CURRENT_CONFIG as config

import click
import numpy as np
from os import path

def count_wins_losses_draws(our_bot_name, summary):
	results = {
		'wins': 0,
		'losses': 0,
		'draws': 0
	}

	for x in summary:
		our_bot = 'X' if x['X'] == our_bot_name else 'O'
		if x['winner'] == our_bot:
			results['wins'] += 1
		elif x['winner'] == 'draw':
			results['draws'] += 1
		else:
			results['losses'] += 1

	return results


@click.command()
@click.option('--data-root')
@click.option('--round')
@click.option('--bot-number')
@click.option('--play-second', is_flag=True)
def play(data_root, round, bot_number, play_second):
	player = config.load_machine_learning_player(path.join(data_root, config.name()), round, bot_number)
	player.training_mode = False
	
	current_guess = 0.5

	for current_level in range(7):
		opponent = CompositePlayer(config.new_benchmark_player(play_second), config.new_random_player(), current_guess)

		rnd = Round(all_v_one_mix([opponent] * 100, player, not play_second, config.empty_board_gen()))
		rnd.play_all()
		
		summary = count_wins_losses_draws(player.name(), rnd.summary())
		print("Played round {}, summary: (wins: {}, draws: {}, losses: {})".format(current_level, summary['wins'], summary['draws'], summary['losses']))
		if summary['wins'] == summary['losses']:
			print("Drew the most maches, final evaluation of this bot playing first is {:.2f}!".format(current_guess))
			break
		elif summary['wins'] > summary['losses']:
			current_guess += (0.5 / (np.power(2, current_level + 1)))
		else:
			current_guess -= (0.5 / (np.power(2, current_level + 1)))
		print('Completed current level, evaulation of bot ability playing first is {:.2f}!'.format(current_guess))


if __name__ == '__main__':
	play()
