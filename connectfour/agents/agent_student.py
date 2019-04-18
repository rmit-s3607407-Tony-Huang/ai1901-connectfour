from connectfour.agents.computer_player import Agent
import math

PLAYER0 = 0
PLAYER1 = 1
PLAYER2 = 2
WINDOW_LENGTH = 4


class StudentAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 5

    def get_move(self, board):
        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, 1, -math.inf, math.inf) )
        #print("Player", self.id, max(vals))
        bestMove = moves[vals.index( max(vals) )]
        return bestMove

    # Goal return column with maximized scores of all possible next states
    def dfMiniMax(self, board, depth, alpha, beta):
        # Check to see if there is a winning move, so it won't evaluate nodes that are deeper than needed
        if self.id == PLAYER2:
            opponent = PLAYER1
        else:
            opponent = PLAYER2

        if self.checkWinningMove(board, self.id):
            return 10000000000
        elif self.checkWinningMove(board, opponent):
            return -10000000000

        # Return Heuristic value of the board at the bottom of the tree
        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        # Branch the tree down to the max depth
        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])
                
            moves.append( move )
            vals.append( self.dfMiniMax(next_state, depth + 1, alpha, beta) )

            # Alpha Beta Pruning
            if depth % 2 == 1:
                beta = min(min(vals), beta)
                if alpha >= beta:
                    break
            else:
                alpha = max(alpha, max(vals))
                if alpha >= beta:
                    break

        # Return the Best Value for Max/Min
        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

    # Returns a heuristic value on the board state
    def evaluateBoardState(self, board):
        score = 0

        # Prioritise playing in the center column
        count = 0
        for row in board.board:
            if row[3] == self.id:
                count += 1
        score += count*50

        # Scoring is done by extracting window of 4 and passing it through a function to return a score
        # Score Horizontal
        for row in board.board:
            for col in range(board.width-3):
                window = row[col:col+WINDOW_LENGTH]
                score += self.evaluateWindowState(window, self.id)

        # Score Vertical
        for col in range(board.width):
            temp_column = list()
            temp_column.clear()
            for row in range(board.height):
                temp_column.append(board.board[row][col])
            for j in range(board.height - 3):
                window = temp_column[j: j+WINDOW_LENGTH]
                score += self.evaluateWindowState(window, self.id)

        # Score Diagonal Up
        for col in range(board.width + 1 - WINDOW_LENGTH):
            for row in range(board.height + 1 - WINDOW_LENGTH):
                window.clear()
                for i in range(WINDOW_LENGTH):
                    window.append(board.board[board.height - 1 - row - i][col + i])
                score += self.evaluateWindowState(window, self.id)

        # Score Diagonal Down
        for col in range(board.width + 1 - WINDOW_LENGTH):
            for row in range(board.height + 1 - WINDOW_LENGTH):
                window.clear()
                for i in range(WINDOW_LENGTH):
                    window.append(board.board[row+i][col+i])
                score += self.evaluateWindowState(window, self.id)

        return score

    # Checks the window of 4 and if there is a chance of that window to win, then return a value
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

    # Check to see if a player has already won
    def checkWinningMove(self, board, player):
        # Check Rows
        for row in board.board:
            for col in range(board.width-3):
                window = row[col:col+WINDOW_LENGTH]
                if window.count(player) == 4:
                    return True

        # Check Horizontal
        for col in range(board.width):
            temp_column = list()
            temp_column.clear()
            for row in range(board.height):
                temp_column.append(board.board[row][col])
            for j in range(board.height - 3):
                window = temp_column[j: j + WINDOW_LENGTH]
                if window.count(player) == 4:
                    return True

        # Check Diagonal Up
        for col in range(board.width + 1 - WINDOW_LENGTH):
            for row in range(board.height + 1 - WINDOW_LENGTH):
                window.clear()
                for i in range(WINDOW_LENGTH):
                    window.append(board.board[board.height - 1 - row - i][col + i])
                if window.count(player) == 4:
                    return True

        # Check Diagonal Down
        for col in range(board.width + 1 - WINDOW_LENGTH):
            for row in range(board.height + 1 - WINDOW_LENGTH):
                window.clear()
                for i in range(WINDOW_LENGTH):
                    window.append(board.board[row + i][col + i])
                if window.count(player) == 4:
                    return True

        return False
