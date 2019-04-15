import random

from connectfour.agents.monte_carlo import Node, MTCS
from connectfour.agents.agent import Agent

MAX_DEPTH = 3


class MonteCarloAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def get_move(self, board):
        best_move = self.find_best_move(board)
        return self._find_move_from_new_board_state(board.board, best_move.state.board)

    def find_best_move(self, board, factor=2.0):
        """
        Returns the best move using MonteCarlo Tree Search
        """
        o = Node(board)
        return MTCS(MAX_DEPTH, o, factor, self.id)

    def _find_move_from_new_board_state(self, old, new):
        """
        Making a move in Connect Four makes exactly one change to the board.
        Searching through all x,y positions for a difference between the old and
        new board will tell us exactly where a move was made.
        """
        for x in range(len(old)):
            for y in range(len(old[0])):
                if old[x][y] != new[x][y]:
                    return x, y

        # there is no difference between old and new board states
        return -1, -1


class RandomAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def get_move(self, board):
        """
        RandomAgent always returns a valid (ie. partially empty) column to place token in
        """
        while True:
            col = random.randint(0, board.width)
            row = board.try_move(col)

            if row >= 0:
                break

        return row, col
