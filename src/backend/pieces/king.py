from io import DEFAULT_BUFFER_SIZE
from .piece import Piece
from .pawn import Pawn

class King(Piece):
    ID = 1
    def __init__(self, is_white, location):
        super().__init__(is_white, location)
        self.ID = King.ID
        self.value = 100
        King.ID += 1

    def __str__(self):
        return 'K' if self.is_white else 'k'

    def value(self):
        return 100

    def is_valid_move(self, board, destination):
        x_dir = abs(self.location[0] - destination[0])
        y_dir = abs(self.location[1] - destination[1])
        if x_dir > 1 or  y_dir > 1:
            return False
        elif self.is_white is board[destination].is_white:
            return False
        else:
            for piece in (pieces := board.black_pieces if self.is_white else board.white_pieces):
                #Edge case for pawn check
                if isinstance(piece, Pawn):
                    direction = 1 if piece.is_white else -1
                    if piece.location[0] + direction == destination[0] and piece.location[1] + direction == destination[1]:
                        return False
                elif piece.is_white is not self.is_white and (destination[0]*10 + destination [1]) in piece.moves(board):
                    return False
        return True

    def moves(self, board):
        result = set()
        possible_location = {piece.location[0]*10 + piece.location[1] \
            for row in range(-1, 2) for col in range(-1, 2) if (row or col) and (piece := board[self.location[0]+row*10, self.location[1]+col])}
        opposing_attacks = set()
        for piece in (pieces := board.black_pieces if self.is_white else board.white_pieces):
            if ...: # need to implement edge case for pawn
                ...
            else:
                opposing_attacks.add(piece.move(board))
        result = possible_location - opposing_attacks
        return result



    def checkmate(self, board):
        return False

