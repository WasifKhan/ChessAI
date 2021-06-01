'''
Auxiliary functions for Advanced CNN
'''

from numpy import array



def move_to_datapoint(board, piece):
    datapoint = [0]*len(piece.move_IDs)
    for i, ID in enumerate(piece.move_IDs):
        piece_move = piece.move_IDs[ID](piece.location)
        piece_move = (piece_move//10, piece_move%10)
        if piece_move[0] >= 0 and piece_move[0] <= 7 \
                and piece_move[1] >= 0 and piece_move[1] <= 7 \
                and board.is_valid_move(piece, piece_move):
            datapoint[i] = 0.65
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
                dp = array([ID/10, value/10, piece.defends/10,
                    piece.threats/10, piece.threatens/10,
                    piece.num_moves/10])
                cur_row.append(dp)
            cur_row = array(cur_row)
            datapoint.append(cur_row)
        is_white = not(is_white)
        datapoint = array(datapoint)
        datapoints.append(datapoint)
    datapoints = array(datapoints)
    datapoints = datapoints.reshape((datapoints.shape[0], 8, 8, 6))
    return datapoints

def moves_to_datapoints(boards, moves):
    piece_map = {'P': 0, 'B': 8, 'N': 10, 'R': 12, 'Q': 14, 'K':15}
    piece_datapoints = list()
    board_datapoints = list()
    is_white = True
    for i, board in enumerate(boards):
        piece = boards[i][moves[i][0]]
        piece_datapoint = [0]*16
        piece_datapoint[piece_map[str(piece).upper()] + piece.ID - 1] = 1
        piece_datapoint = array(piece_datapoint)
        piece_datapoints.append(piece_datapoint)
        
        board_datapoint = [0]*16
        pieces = boards[i].white_pieces if is_white else boards[i].black_pieces
        for i in range(16):
            board_datapoint[i] = [0]*6
            board_datapoint[i] = array(board_datapoint[i])
        for piece in pieces:
            piece.compute_info(board)
            ID = piece.ID if piece.is_white is not None else 0
            value = piece.value if piece.is_white == is_white \
                    else piece.value * -1
            piece_info = [ID/10, value/10, piece.defends/10,
                    piece.threats/10, piece.threatens/10,
                    piece.num_moves/10]
            piece_info = array(piece_info)
            board_datapoint[piece_map[str(piece).upper()] + piece.ID - 1] = piece_info
        board_datapoint = array(board_datapoint)
        board_datapoint.reshape((1, 16, 6))
        board_datapoints.append(board_datapoint)
    return board_datapoints, piece_datapoints

