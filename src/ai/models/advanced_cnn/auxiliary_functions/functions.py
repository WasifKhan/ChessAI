'''
Auxiliary Functions for Basic CNN
'''

from numpy import array
from copy import copy


def move_to_datapoint(board, piece):
    datapoint = [0]*len(piece.move_IDs)
    for i, ID in enumerate(piece.move_IDs):
        piece_move = piece.move_IDs[ID](piece.location)
        piece_move = (piece_move//10, piece_move%10)
        if piece_move[0] >= 0 and piece_move[0] <= 7 \
                and piece_move[1] >= 0 and piece_move[1] <= 7 \
                and board.is_valid_move(piece, piece_move):
            temp_board = copy(board)
            temp_board.move(temp_board[piece.location], piece_move)
            datapoint[i] = piece.compute_info(board)
    datapoint = array(datapoint)
    return datapoint


def boards_to_datapoints(boards):
    is_white = True
    datapoints = []
    for board in boards:
        board_direction = range(8) if is_white else range(7, -1, -1)
        datapoint = []
        for row in board_direction:
            cur_row = []
            for column in range(8):
                piece = board[column,row]
                piece.compute_info(board)
                ID = piece.ID if piece.is_white is not None else 0
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
    datapoints = array(datapoints)
    datapoints = datapoints.reshape((datapoints.shape[0], 8, 8, 5))
    return datapoints

def moves_to_datapoints(boards, moves, info):
    from copy import copy
    piece_map = {'P': 0, 'B': 8, 'N': 10, 'R': 12, 'Q': 14, 'K':15}
    datapoints = [0] * len(boards)
    white_turn = True
    bad_indicies = []
    for i, board in enumerate(boards):
        datapoints[i] = array([0]*16)
        real_piece = boards[i][moves[i][0]]
        ID = real_piece.ID if real_piece.value != 9 else 1
        real_piece_ID = str(real_piece) + str(ID)
        real_move = moves[i][1]
        my_pieces = board.white_pieces if white_turn else board.black_pieces
        found = False
        for piece in my_pieces:
            ID = piece.ID if piece.value != 9 else 1
            move_ID = info[i][piece_map[str(piece).upper()] + ID - 1]
            if str(piece) + str(ID) == real_piece_ID:
                our_move = piece.move_IDs[move_ID](piece.location)
                if our_move == real_move:
                    datapoints[i][piece_map[str(piece).upper()] + ID - 1] = 1
                    found = True
                break
        if not found:
            bad_indicies.append(i)
        white_turn = not(white_turn)
    for index in bad_indicies[::-1]:
        del datapoints[index]
    datapoints = array(datapoints)
    return datapoints, bad_indicies

