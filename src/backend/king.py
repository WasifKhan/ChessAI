from .piece import Piece


class King(Piece):
    ID = 1
    def __init__(self, is_white, location):
        super().__init__(is_white, location)
        self.ID = King.ID
        King.ID += 1

    def __str__(self):
        return '$' if self.is_white else '-'

    def is_valid_move(self, board, destination):
        return True

    def moves(self):
        raise NotImplementedError

