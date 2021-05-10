'''
Baseline AI performing random moves
'''

from ai.models.base_ai import AI
from random import randint



class RandomAI(AI):
    def __init__(self, location):
        super().__init__(location)

    def _trained(self):
        return True

    def _predict_move(self, board, is_white):
        my_pieces = list(board.white_pieces) if is_white else list(board.black_pieces)
        rand_piece = randint(0, max(0, len(my_pieces) - 1))
        while len(my_pieces[rand_piece].moves(board)) == 0:
            rand_piece = randint(0, max(0, len(my_pieces) - 1))
        piece = my_pieces[rand_piece]
        moves = list(piece.moves(board))
        rand_move = randint(0, max(0, len(moves) - 1))
        source = piece.location[0]*10 + piece.location[1]
        destination = moves[rand_move]
        return (source, destination)


