from tictactoe799.match import Match
from tictactoe799.player.human_player import HumanPlayer
from tictactoe799.player.machine_learning_player import load_model
from tictactoe799.player.exhaustive_player import ExhaustivePlayer
from tictactoe799.player.minimax_player import MinimaxPlayer

import click

@click.command()
@click.option('--exhaustive', is_flag=True)
@click.option('--minimax', is_flag=True)
@click.option('--ml', is_flag=True)
@click.option('--round')
@click.option('--bot-number')
@click.option('--play-second', is_flag=True)
def play(exhaustive, minimax, ml, round, bot_number, play_second):
	player = HumanPlayer()
	
	if exhaustive:
		opponent = ExhaustivePlayer()
	elif minimax:
		opponent = MinimaxPlayer(play_second)  # If I am playing second, the bot is playing first
	else:
		opponent = load_model(round, bot_number)
		opponent.training_mode = False

	if not play_second:
		players = [player, opponent]
	else:
		players = [opponent, player]

	match = Match(players)
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
 