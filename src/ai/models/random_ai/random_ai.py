'''
Baseline AI performing random moves
'''

from ai.data.model_info import ModelInfo
from random import randint



class RandomAI(ModelInfo):
    def __init__(self, game, location):
        super().__init__(game, location)


    def _predict(self, board, is_white):
        my_pieces = list(board.white_pieces) if is_white else list(board.black_pieces)
        while True:
            rand_piece = randint(0, len(my_pieces) - 1)
            piece = my_pieces[rand_piece]
            moves = list(piece.moves(board))
            if moves:
                rand_move = randint(0, len(moves) - 1)
                source = piece.location[0]*10 + piece.location[1]
                destination = moves[rand_move]
                if board.is_valid_move(piece, (destination//10, destination%10)):
                    return (source, destination)


