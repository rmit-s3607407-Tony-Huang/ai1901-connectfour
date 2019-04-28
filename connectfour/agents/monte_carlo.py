import copy
import math
import random


class Node:
    """
    Data structure to keep track of our search
    """

    def __init__(self, state, parent=None):
        self.visits = 1
        self.reward = 0.0
        self.state = state
        self.children = []
        self.children_move = []
        self.parent = parent

    def add_child(self, child_state, move):
        child = Node(child_state, self)
        self.children.append(child)
        self.children_move.append(move)

    def update(self, reward):
        self.reward += reward
        self.visits += 1

    def fully_explored(self):
        if len(self.children) == len(self.state.legal_moves()):
            return True
        return False


def MTCS(maxIter, root, factor, player_id):
    """
    Args:
        maxIter: How many iterations to run the search for
        root: The `Node` object that begins the search. Is at first the current state of board.
        factor: ?? (unknown)
        player_id: The id of the player, which will be used to mark a token placement

    Returns:
        A new instance of `Board` that includes the best move found.
    """
    for _ in range(maxIter):
        front, turn = tree_policy(root, player_id, factor)
        reward = default_policy(front.state, turn)
        backup(front, reward, turn)

    ans = best_child(root, 0)
    # print([(c.reward / c.visits) for c in ans.parent.children])
    return ans


def tree_policy(node, turn, factor):
    while not node.state.terminal() and node.state.winner() == 0:
        if not node.fully_explored():
            return expand(node, turn), -turn
        else:
            node = best_child(node, factor)
            turn *= -1
    return node, turn


def expand(node, turn):
    tried_children_move = [m for m in node.children_move]
    possible_moves = node.state.legal_moves()

    for move in possible_moves:
        if move not in tried_children_move:
            row = node.state.try_move(move)
            new_state = copy.deepcopy(node.state)
            new_state.board[row][move] = turn
            new_state.last_move = [row, move]
            break

    node.add_child(new_state, move)
    return node.children[-1]


def best_child(node, factor):
    bestscore = -10000000.0
    best_children = []
    for c in node.children:
        exploit = c.reward / c.visits
        explore = math.sqrt(math.log(2.0 * node.visits) / float(c.visits))
        score = exploit + factor * explore
        if score == bestscore:
            best_children.append(c)
        if score > bestscore:
            best_children = [c]
            bestscore = score
    return random.choice(best_children)


def default_policy(state, turn):
    count = 100
    while not state.terminal() and state.winner() == 0 and count > 0:
        state = state.next_state_rand(turn)
        turn *= -1
        count -= 1
    return state.winner()


def backup(node, reward, turn):
    while node is not None:
        node.visits += 1
        node.reward -= turn * reward
        node = node.parent
        turn *= -1
    return
