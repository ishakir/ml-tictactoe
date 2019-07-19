import click
import csv

from mlgames.board import Board

class Node:
	def __init__(self, board, parent, us_to_play):
		self.board = board
		self.parent = parent
		self.us_to_play = us_to_play
		self.result = None

		self.total_results = 0
		if not board.full() and not board.winner():
			for x in range(3):
				for y in range(3):
					if not self.board.taken(x, y):
						self.total_results += 1
		else:
			self.total_results = 1

		self.results = []

	def report_result(self, val):
		self.results.append(val)
		if len(self.results) == self.total_results:
			cumulative_result = max(self.results) if self.us_to_play else min(self.results)
			self.result = cumulative_result
			if self.parent:
				self.parent.report_result(cumulative_result)

@click.command()
def run():
	first_node = Node(Board([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]), None, True)
	# first_node = Node(Board([['.', '.', 'X'], ['O', 'X', 'O'], ['X', 'O', 'X']]), None, False)

	stack = []
	stack.append(first_node)

	all_nodes = []

	while not len(stack) == 0:
		node = stack.pop(0)
		all_nodes.append(node)
		if len(all_nodes) % 1000 == 0:
			print("Explored {} nodes, stack depth {}".format(str(len(all_nodes)), str(len(stack))))
		winner = node.board.winner()
		if winner == 'X':
			node.report_result(1)
		elif winner == 'O':
			node.report_result(-1)
		elif node.board.full():
			node.report_result(0)
		else:
			for x in range(3):
				for y in range(3):
					if not node.board.taken(x, y):
						new_board = node.board.place('X' if node.us_to_play else 'O', x, y)
						stack.append(Node(new_board, node, not node.us_to_play))

	with open('minimax_state.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['board_state', 'result'])
		for node in all_nodes:
			if node.result is None:
				print("{}, {}, {}, {}".format(node.board.to_single_line_string(), node.total_results, node.results, node.us_to_play))
			writer.writerow([node.board.to_single_line_string(), node.result])


if __name__ == '__main__':
	run()
