from .piece import Piece


class Knight(Piece):
    def __init__(self, ID, is_white, location):
        super().__init__(is_white, location)
        self.ID = ID
        self.value = 3

    def __str__(self):
        return 'N' if self.is_white else 'n'

    def _initialize_moves(self):
        direction = 1 if self.is_white else -1
        self.move_IDs[0] = lambda location: \
                (location[0] + 2)*10 + location[1] + 1*direction
        self.move_IDs[1] = lambda location: \
                (location[0] + 2)*10 + location[1] - 1*direction
        self.move_IDs[2] = lambda location: \
                (location[0] - 2)*10 + location[1] + 1*direction
        self.move_IDs[3] = lambda location: \
                (location[0] - 2)*10 + location[1] - 1*direction
        self.move_IDs[4] = lambda location: \
                (location[0] + 1)*10 + location[1] + 2*direction
        self.move_IDs[5] = lambda location: \
                (location[0] + 1)*10 + location[1] - 2*direction
        self.move_IDs[6] = lambda location: \
                (location[0] - 1)*10 + location[1] + 2*direction
        self.move_IDs[7] = lambda location: \
                (location[0] - 1)*10 + location[1] - 2*direction

    def is_valid_move(self, board, destination):
        vertical_move = abs(destination[0] - self.location[0])
        horizontal_move = abs(destination[1] - self.location[1])

        if not(vertical_move == 1 and horizontal_move == 2) and not(vertical_move == 2 and horizontal_move == 1):
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
        if (piece := board[self.location[0]+1, self.location[1]+2]) and piece.is_white is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]-1, self.location[1]+2]) and piece.is_white is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]+1, self.location[1]-2]) and piece.is_white is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]-1, self.location[1]-2]) and piece.is_white is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]+2, self.location[1]+1]) and piece.is_white is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]-2, self.location[1]+1]) and piece.is_white is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]+2, self.location[1]-1]) and piece.is_white is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        if (piece := board[self.location[0]-2, self.location[1]-1]) and piece.is_white is not self.is_white:
            result.add(piece.location[0]*10 + piece.location[1])
        return result

