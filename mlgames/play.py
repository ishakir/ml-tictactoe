from mlgames.config.active_config import CURRENT_CONFIG as config

from mlgames.match import Match

import click

@click.command()
@click.option('--data-root', default='.')
@click.option('--benchmark', is_flag=True)
@click.option('--random', is_flag=True)
@click.option('--ml', is_flag=True)
@click.option('--round')
@click.option('--bot-number')
@click.option('--play-second', is_flag=True)
def play(data_root, benchmark, random, ml, round, bot_number, play_second):
	player = config.new_human_player()

	if random:
		opponent = config.new_random_player()
	elif benchmark:
		opponent = config.new_benchmark_player(play_second) # If I am playing second, the bot is playing first
	elif ml:
		opponent = config.load_machine_learning_player(data_root, round, bot_number)
		opponent.training_mode = False

	if not play_second:
		players = [player, opponent]
	else:
		players = [opponent, player]

	match = Match(players, config.empty_board_gen)
	while not match.is_finished():
		print('Current state: ')
		print(str(match.current_board))
		print()
		print('{} is next to play:'.format(match.next_to_play()))
		match.play_next()

	print(str(match.current_board))
	print('Winner is {}'.format(match.winner()))


if __name__ == '__main__':
	play()
 