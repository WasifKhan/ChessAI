'''
Auxiliary Functions for Basic CNN
'''

from numpy import array
from copy import copy
from ai.models.cnn_basic.moves import MOVES as MOVES

def boards_to_datapoints(boards, white=True):
    is_white = white
    datapoints = []
    for board in boards:
        board_direction = range(8) if is_white else range(7, -1, -1)
        datapoint = []
        for row in board_direction:
            cur_row = []
            for column in range(8):
                piece = board[column,row]
                piece.compute_info(board)
                value = piece.value if piece.is_white == is_white \
                        else piece.value * -1
                dp = array([value, piece.defends,
                    piece.threats, piece.threatens,
                    piece.num_moves])
                cur_row.append(dp)
            cur_row = array(cur_row)
            datapoint.append(cur_row)
        is_white = not(is_white)
        datapoint = array(datapoint)
        datapoints.append(datapoint)
    return datapoints

def moves_to_datapoints(boards, data):
    datapoints = [0] * len(boards)
    bad_indicies = []
    white_turn = True
    for i, board in enumerate(boards):
        datapoint = array([-1]*142)
        my_pieces = board.white_pieces if white_turn else board.black_pieces
        num_states = 0
        valid_moves = 0
        best_move = 0
        for piece in my_pieces:
            source = piece.location[0]*10 + piece.location[1]
            for move in piece.move_IDs:
                temp_board = copy(board)
                destination = piece.move_IDs[move](piece.location)
                destination = (destination//10, destination%10)
                if destination[0] >= 0 and destination[0] <= 7 \
                        and destination[1] >= 0 and destination[1] <= 7 \
                        and temp_board.is_valid_move(temp_board[source], destination):
                    temp_board.move(temp_board[source], destination)
                    if (index := repr(temp_board)) in data[i+1]:
                        num_boards = data[i+1][index]
                        best_move = max(num_boards, best_move)
                        num_states += num_boards
                        valid_moves += 1
                        move_index = MOVES[temp_board.move_ID]
                        datapoint[move_index] = num_boards
        if num_states == 0:
            bad_indicies.append(i)
        else:
            datapoint = datapoint / best_move
            datapoints[i] = datapoint
        white_turn = not(white_turn)
    return datapoints, bad_indicies

