import math
import sys
from typing import Set

"""
Tic Tac Toe Player
"""
# TODO - Implement the following functions (made magic came true):


X: str = "X"
O: str = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board) -> str:
    """
    Returns player who has the next turn on a board.
    """
    # First turn is always X
    if board == initial_state():
        return X

    # Count X and O
    count_x: int = count_value_in_2d_array(board, X)
    count_o: int = count_value_in_2d_array(board, O)

    if count_x > count_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_actions = set()

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] is None:
                available_actions.add((i, j))

    return available_actions


def result(board, action: tuple):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action")
    # TODO: delete it
    if action not in actions(board):
        raise Exception("Invalid action")

    new_board = [row[:] for row in board]

    current_player = player(board)
    new_board[action[0]][action[1]] = current_player
    return new_board


def winner(board: tuple) -> str:
    """
    Returns the winner of the game, if there is one.
    """
    n = len(board)

    # check each rows for winner
    for row in board:
        if all(cell == row[0] and cell is not None for cell in row):
            return row[0]

    # check columns for winner
    for column in range(n):
        if all(board[row][column] == board[0][column] and board[row][column] is not None
               for row in range(n)):
            return board[0][column]

    # Check diagonals
    if all(board[i][i] == board[0][0] and board[i][i] is not None
           for i in range(n)):
        return board[0][0]

    if all(board[i][n - 1 - i] == board[0][n - 1] and board[i][n - 1 - i] is not None
           for i in range(n)):
        return board[0][n - 1]

    return None  # no winner


def terminal(board) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    elif not is_value_present(board, None):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        winner_result = winner(board)
        if winner_result is X:
            return 1
        elif winner_result is O:
            return -1
        return 0


# TODO: find why action is NONE
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    available_actions = actions(board)
    made_turns = list()

    # The maximizing player picks action a in Actions(s)
    # that produces the highest value of Min-Value(Result(s, a)).
    if current_player == X:
        for action in available_actions:
            made_turns.append([min_value(result(board, action)), action])

        return max(made_turns)[1]

    # let consider that this player will be min
    if current_player == O:
        for action in available_actions:
            made_turns.append([max_value(result(board, action)), action])

        return min(made_turns)[1]


def is_value_present(board, target_value) -> bool:
    board_len = len(board)

    for row_index in range(board_len):
        for column_index in range(board_len):
            if board[row_index][column_index] == target_value:
                return True

    return False


def max_value(board) -> int:
    value = -sys.maxsize - 1

    if terminal(board):
        return utility(board)

    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    return value


def min_value(board) -> int:
    value = sys.maxsize

    if terminal(board):
        return utility(board)

    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value


def count_value_in_2d_array(array_2d: [[]], target_value) -> int:
    count = 0

    for row in array_2d:
        count += row.count(target_value)

    return count
