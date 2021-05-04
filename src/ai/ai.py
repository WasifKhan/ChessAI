'''
Main AI Engine
'''

import random

class AI:
    def __init__(self, level):
        self.level = level

    def get_move(self, board):
        my_pieces = list()
        for piece in board.pieces:
            if not(piece.is_white):
                my_pieces.append(piece)
        rand_piece = random.randint(0, max(0, len(my_pieces) - 1))

        piece = my_pieces[rand_piece]
        moves = list(piece.moves(board))

        rand_move = random.randint(0, max(0, len(moves) - 1))


        source = piece.location[0]*10 + piece.location[1]
        destination = moves[rand_move]
        return (source, destination)

