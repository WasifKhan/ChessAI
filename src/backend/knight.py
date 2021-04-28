from .piece import Piece


class Knight(Piece):
    ID = 1
    def __init__(self, is_white, location):
        super().__init__(is_white, location)
        self.ID = Knight.ID
        Knight.ID += 1

    def __str__(self):
        return 'K' if self.is_white else 'k'

    def is_valid_move(self, board, destination):
        vertical_move = abs(destination[0] - self.location[0])
        horizontal_move = abs(destination[1] - self.location[1])

        if not(vertical_move == 1 and horizontal_move == 2) and not(vertical_move == 2 and horizontal_move == 1):
            print(vertical_move)
            print(horizontal_move)
            return False
        elif not(isinstance(board[destination], Piece)):
            return True
        elif self.is_white and board[destination].is_white:
            return False
        elif not(self.is_white) and not(board[destination].is_white):
            return False
        return True

    def moves(self, board):
        result = set()
        if (piece := board[self.location[0]+1, self.location[1]+2].is_white) is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]-1, self.location[1]+2].is_white) is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]+1, self.location[1]-2].is_white) is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]-1, self.location[1]-2].is_white) is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]+2, self.location[1]+1].is_white) is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]-2, self.location[1]+1].is_white) is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]+2, self.location[1]-1].is_white) is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]-2, self.location[1]-1].is_white) is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        return result

