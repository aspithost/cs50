"""
Tic Tac Toe Player
"""
from copy import deepcopy


X = "X"
O = "O"
EMPTY = None


class Board():
    def __init__(self, _board):
        self.X = X
        self.O = O
        self.EMPTY = EMPTY
        self.counter = {
            self.X: 0,
            self.O: 0,
            self.EMPTY: 0,
        }
        for row in _board:
            if not len(row) == 3:
                raise ValueError("Board needs to be 3x3")
            for tile in row:
                if tile not in [self.X, self.O, self.EMPTY]:
                    raise ValueError("Board can only consist of 'X', 'O', and None")
                self.counter[tile] += 1
        self.board = _board

    @property
    def player(self):
        if self.counter[self.EMPTY] == 0:
            return None
        elif self.counter[self.X] > self.counter[self.O]:
            return self.O
        return self.X

    @property
    def actions(self):
        possible_actions = set()
        for row_index, row in enumerate(self.board):
            for tile_index, tile in enumerate(row):
                if tile == self.EMPTY:
                    possible_actions.add((row_index, tile_index))
        return possible_actions

    @property
    def winner(self):
        for i in range(3):
        # check if there is a horizontal winner
            if self.board[i][0] and all(self.board[i][0] == self.board[i][j] for j in range(1, 3)):
                return self.board[i][0]
            # check if there is a vertical winner
            if self.board[0][i] and all(self.board[0][i] == self.board[j][i] for j in range(1, 3)):
                return self.board[0][i]

        # Check if there is a diagonal winner
        if self.board[1][1]:
            if self.board[0][0] == self.board[1][1] == self.board[2][2] or self.board[0][2] == self.board[1][1] == self.board[2][0]:
                return self.board[1][1]

        return None

    @property
    def terminal(self):
        if self.winner or self.counter[self.EMPTY] == 0:
            return True
        return False

    @property
    def utility(self):
        winner = self.winner
        if winner == self.X:
            return 1
        elif winner == self.O:
            return -1
        return 0

    @property
    def minimax(self):
        board_instance = Board(self.board)
        if board_instance.terminal:
            return None

        is_max_player = True if board_instance.player == board_instance.X else False

        _, action = self.calculate_best_action(is_max_player)
        return action

    def result(self, action):
        row_index, tile_index = action
        board = deepcopy(self.board)
        if 0 <= row_index <= 2 and 0 <= tile_index <= 2:
            current_tile = board[row_index][tile_index]

            # Check if board tile is empty
            if not current_tile:
                # Determine what user's turn it is, and update board copy
                board[row_index][tile_index] = self.player
                return board

        raise Exception("Action not allowed")

    def calculate_best_action(self, is_max_player):
        # Keep track of best move for all possible actions of one board
        best_util = -1 if is_max_player else 1

        for action in self.actions:
            new_board = Board(self.result(action))
            util = new_board.utility
            if new_board.terminal:
                return util, action

            # If player X wins or player O wins in their own turn, return from function
            if (is_max_player and util == 1) or (not is_max_player and util == -1):
                return util, action

            new_util, action = new_board.calculate_best_action(not is_max_player)
            # If move represents better utility for a player, update the utility
            if (is_max_player and new_util > best_util) or (not is_max_player and new_util < best_util):
                best_util = new_util

        return best_util, action

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    return Board(board).player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return Board(board).actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    return Board(board).result(action)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    return Board(board).winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return Board(board).terminal


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    return Board(board).utility


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    return Board(board).minimax
