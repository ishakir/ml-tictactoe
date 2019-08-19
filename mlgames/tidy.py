import click
from collections import defaultdict
from os import listdir, path, remove
import pandas as pd
from shutil import rmtree

import re

IGNORE_PATHS = set(['.DS_Store', 'lost+found'])

BOT_NAME_REGEX = re.compile('^ML Bot (\d+)$')

def get_number(st):
	m = BOT_NAME_REGEX.match(st)
	return m.group(1)

def preserve_entirely(maximum, number):
	if number == maximum:
		return True
	elif number == 1:
		return True
	elif number < 100 and number % 10 == 0:
		return True
	elif number < 1000 and number % 100 == 0:
		return True
	elif number % 1000 == 0:
		return True
	else:
		return False

def read_file(file):
    results_per_bot = defaultdict(lambda: defaultdict(lambda: 0))
    with open(file, 'r') as f:
        headers = f.readline().strip()
        line = "1"
        while line:
            line = f.readline().strip()
            entries = line.split(",")
            if len(entries) == 4:
                if entries[2] == 'X':
                    results_per_bot[entries[0]]['wins'] += 1
                    results_per_bot[entries[1]]['losses'] += 1
                elif entries[2] == 'O':
                    results_per_bot[entries[1]]['wins'] += 1
                    results_per_bot[entries[0]]['losses'] += 1
                elif entries[2] == 'draw':
                    results_per_bot[entries[0]]['draws'] += 1
                    results_per_bot[entries[1]]['draws'] += 1
                else:
                    raise RuntimeError("wtf")
                
            elif len(entries) != 1:
                print(entries)
                raise RuntimeError("wtf")

    data = []
    for bot_name, results in results_per_bot.items():
    	data.append([bot_name, results['wins'], results['draws'], results['losses']])
    
    return pd.DataFrame(data, columns=['bot_name', 'wins', 'draws', 'losses'])

@click.command()
@click.option('--data-root', default='.')
@click.option('--dry-run', is_flag=True)
def tidy(data_root, dry_run):
	for config in [d for d in listdir(data_root) if d not in IGNORE_PATHS]:
		config_dir = path.join(data_root, config)
		print("Tidying {}".format(config))

		all_round_dirs = sorted([int(i) for i in listdir(config_dir)])
		max_round = max(all_round_dirs)
		to_prune = [path.join(config_dir, str(rnd)) for rnd in all_round_dirs if not preserve_entirely(max_round, rnd)]

		for round_dir in to_prune:
			round_robin_dir = path.join(round_dir, 'round_robin')
			players_dir = path.join(round_dir, 'starting_players')
			benchmark_dir = path.join(round_dir, 'benchmark')
			training_log_dir = path.join(round_dir, 'training_log')

			bot_results = read_file(path.join(round_robin_dir, 'results_summary.csv'))

			winner = bot_results.sort_values('wins', ascending=False).iloc[0].bot_name
			drawer = bot_results.sort_values('draws', ascending=False).iloc[0].bot_name
			loser = bot_results.sort_values('losses', ascending=False).iloc[0].bot_name

			winner_number = get_number(winner)
			drawer_number = get_number(drawer)
			loser_number = get_number(loser)

			print("Now pruning {}: (Winner: {}, Drawer: {}, Loser: {})".format(round_dir, winner, drawer, loser))
			if not dry_run:
				if path.exists(training_log_dir):
					rmtree(path.join(round_dir, 'training_log'))

				for x in listdir(round_robin_dir):
					if x == 'results_summary.csv':
						continue
					elif (winner in x and drawer in x) or (drawer in x and loser in x) or (loser in x and winner in x):
						continue
					else:
						remove(path.join(round_robin_dir, x))

				for x in listdir(benchmark_dir):
					if x == 'results_summary.csv':
						continue
					elif winner in x or drawer in x or loser in x:
						continue
					else:
						remove(path.join(benchmark_dir, x))

				for x in listdir(players_dir):
					if (x == '{}.h5'.format(winner_number)) or (x == '{}.h5'.format(drawer_number)) or (x == '{}.h5'.format(loser_number)):
						continue
					else:
						remove(path.join(players_dir, x))


if __name__ == '__main__':
	tidy()
