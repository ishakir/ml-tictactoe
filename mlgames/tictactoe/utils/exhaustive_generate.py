import click
import csv

from mlgames.board import Board

class Node:
	def __init__(self, board, parent, next_to_play):
		self.board = board
		self.parent = parent
		self.next_to_play = next_to_play

		self.this_player_wins_count = 0
		self.draws = 0
		self.this_player_loses_count = 0

	def this_player_wins(self):
		self.this_player_wins_count += 1
		if self.parent:
			self.parent.this_player_loses()

	def draw(self):
		self.draws += 1
		if self.parent:
			self.parent.draw()

	def this_player_loses(self):
		self.this_player_loses_count += 1
		if self.parent:
			self.parent.this_player_wins()

TYPES = ['X', 'O']

@click.command()
def run():
	first_node = Node(Board([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]), None, 0)

	stack = []
	stack.append(first_node)

	all_nodes = []

	while not len(stack) == 0:
		node = stack.pop(0)
		all_nodes.append(node)
		if len(all_nodes) % 1000 == 0:
			print("Explored {} nodes, stack depth {}".format(str(len(all_nodes)), str(len(stack))))
		winner = node.board.winner()
		if winner:
			node.this_player_wins()
		elif node.board.full():
			node.draw()
		else:
			for x in range(3):
				for y in range(3):
					if not node.board.taken(x, y):
						new_board = node.board.place(TYPES[node.next_to_play], x, y)
						stack.append(Node(new_board, node, (node.next_to_play + 1) % 2))

	with open('exhaustive_state.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['board_state', 'this_player_wins', 'draws', 'this_player_loses'])
		for node in all_nodes:
			writer.writerow([node.board.to_single_line_string(), node.this_player_wins_count, node.draws, node.this_player_loses_count])


if __name__ == '__main__':
	run()
