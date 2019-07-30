from abc import ABC, abstractmethod

class Board(ABC):
	# piece should be a player signifier (e.g. X or O)
	# move should be whatever type you chose move to be (e.g. (x, y))
	# 
	# Should return new version of same type (another Board)
	@abstractmethod
	def play(self, piece, move):
		pass

	# Should return the winner's 'piece', None if no winner
	@abstractmethod
	def winner(self):
		pass

	# Should return a parsed representation from a string passed via the command line
	@abstractmethod
	def parse_move(self, move_str):
		pass

	# piece should be a player signifier (e.g. X or O)
	# move should be whatever type you chose move to be (e.g. (x, y))
	# 
	# Should return a boolean indicating whether the suggested move is legal
	@abstractmethod
	def play_is_legal(self, piece, move):
		pass

	# Should return a list of all the currently legal moves that this piece can play
	@abstractmethod
	def all_legal_moves(self, piece):
		pass

	# Should return whether the board is 'complete' (i.e. no more moves are possible)
	#
	# n.b. this is always paired with winner() so it doesn't really matter what this returns in the
	# case where there's a winner - it's mostly used for detecting 'draw' states
	@abstractmethod
	def complete(self):
		pass

	# Should return all equivalent states of this board along all symmetries, along with the respective
	# equivalent move under those same symmetries 
	@abstractmethod
	def all_symmetries(self, move):
		pass

	# Human readable to string
	@abstractmethod
	def __str__(self):
		pass

	# Single line to string suitable for, say, easy csv storage
	def to_single_line_string(self):
		pass
