from .piece import Piece


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

        if x_dir == 0 and y_dir == 0:
            return False
        elif x_dir > 1 or  y_dir > 1:
            return False
        else:
            for piece in board.pieces:
                if piece.is_white is not self.is_white and destination not in piece.moves(board):
                    return False
        return True

    def moves(self, board):
        return set()

