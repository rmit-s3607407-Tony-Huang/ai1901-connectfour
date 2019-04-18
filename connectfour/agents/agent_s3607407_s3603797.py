from connectfour.agents.computer_player import Agent
import random
import math

PLAYER0 = 0
PLAYER1 = 1
PLAYER2 = 2
WINDOW_LENGTH = 4


class StudentAgent1(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 5

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
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, 1, -math.inf, math.inf) )

        bestMove = moves[vals.index( max(vals) )]
        return bestMove

    def dfMiniMax(self, board, depth, alpha, beta):
        # Goal return column with maximized scores of all possible next states
        
        #if depth == self.MaxDepth:
            #print('player', self.id, self.evaluateBoardState(board))
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            #print(move)
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])
                
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1, alpha, beta) )

            #for row in board.board:
            #    print(row)
            print(vals)

            if depth % 2 == 1:
                beta = min(min(vals), beta)
                print('beta = ', beta)
                if alpha >= beta:
                    break
            else:
                alpha = max(alpha, max(vals))
                print('alpha = ', alpha)
                if alpha >= beta:
                    break

        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

    def evaluateBoardState(self, board):
        score = 0

        ##Skew Middle Rows
        count = board.board[2].count(self.id)
        count1 = board.board[3].count(self.id)
        count2 = 0
        count3 = 0
        count4 = 0

        ##Skew Middle Column
        for row in board.board:
            if row[2] == self.id:
                count2+1
            if row[3] == self.id:
                count3+1
            if row[4] == self.id:
                count4+1

        #score += count*2 + count1*2 + count2*3 + count3*8 + count4*3

        ##Score Horizontal
        for row in board.board:
            for col in range(board.width-3):
                window = row[col:col+WINDOW_LENGTH]
                score += self.evaluateWindowState(window, self.id)

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
        for col in range(board.width + 1 - WINDOW_LENGTH):
            for row in range(board.height + 1 - WINDOW_LENGTH):
                window.clear()
                for i in range(WINDOW_LENGTH):
                    window.append(board.board[board.height - 1 - row - i][col + i])
                score += self.evaluateWindowState(window, self.id)
                #print(window)

        ##Score Diagonal Down
        for col in range(board.width + 1 - WINDOW_LENGTH):
            for row in range(board.height + 1 - WINDOW_LENGTH):
                window.clear()
                for i in range(WINDOW_LENGTH):
                    window.append(board.board[row+i][col+i])
                score += self.evaluateWindowState(window, self.id)

        '''for row in board.board:
            print(row)
        print('score = ', score)'''
        return score

    def evaluateWindowState(self, window, player):
        score = 0

        if player == PLAYER2:
            opponent = PLAYER1
        else:
            opponent = PLAYER2

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
