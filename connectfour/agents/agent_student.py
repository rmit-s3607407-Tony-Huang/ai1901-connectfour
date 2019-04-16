from connectfour.agents.computer_player import Agent
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4

PLAYER0 = 0
PLAYER1 = 1
PLAYER2 = 2


class StudentAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 3


    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """
        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            #print(move)
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, 1) )

        bestMove = moves[vals.index( max(vals) )]
        return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states
        
        if depth == self.MaxDepth:
            print('player', self.id, self.evaluateBoardState(board))
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])
                
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1) )

        
        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

    def evaluateBoardState(self, board):
        """
        Your evaluation function should look at the current state and return a score for it. 
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """
        
        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """
        score = 0

        ##Skew Middle Rows
        count = board.board[2].count(self.id)
        count1 = board.board[3].count(self.id)
        count2 = 0
        count3 = 0
        count4 = 0

        score += count*2 + count1*2

        ##Skew Middle Column
        for row in board.board:
            #print(row[1])
            if row[2]==self.id:
                count2+1
            if row[3]==self.id:
                count3+1
            if row[4]==self.id:
                count4+1

        score += count2*3 + count3*8 + count4*3


        ##Score Horizontal
        for row in board.board:
            #print('\n')
            for col in range(board.width-3):
                window = row[col:col+WINDOW_LENGTH]
                score += self.evaluateWindowState(window, self.id)
                # print(window)
        #print('\n')
        ##Score Vertical

        for col in range(board.width):
            temp_column = list()
            temp_column.clear()
            for row in range(board.height):
                temp_column.append(board.board[row][col])
            for j in range(board.height - 3):
                window = temp_column[j: j+WINDOW_LENGTH]
                score += self.evaluateWindowState(window, self.id)
                #print(window)

        ##Score Diagonal Up

        ##Score Diagonal Down
        #print('score = ' )
        #print(score)
        #print('\n')
        return score

    def evaluateWindowState(self, window, player):
        score = 0

        opponent = PLAYER2
        if player == PLAYER2:
            opponent = PLAYER1

        if window.count(player) == 4:
            score += 1000
        elif window.count(player) == 3 and window.count(PLAYER0) == 1:
            score += 100
        elif window.count(player) == 2 and window.count(PLAYER0) == 2:
            score += 10

        if window.count(opponent) == 4:
            score -= 1000
        elif window.count(opponent) == 3 and window.count(PLAYER0) == 1:
            score -= 100
        elif window.count(opponent) == 2 and window.count(PLAYER0) == 2:
            score -= 10

        return score
