from .piece import Piece


class Bishop(Piece):
    ID = 1
    def __init__(self, is_white, location):
        super().__init__(is_white, location)
        self.ID = Bishop.ID
        self.value = 3
        Bishop.ID += 1

    def __str__(self):
        return 'B' if self.is_white else 'b'

    def value(self):
        return 3

    def is_valid_move(self, board, destination):
        x_direction = destination[0] - self.location[0]
        y_direction = destination[1] - self.location[1]
        x_plane = 1 if x_direction > 0 else -1
        y_plane = 1 if y_direction > 0 else -1
        if abs(x_direction) != abs(y_direction):
            return False
        for i in range(1, x_direction):
            if not(board[self.location[0] + (i * x_plane), self.location[1] + (i*y_plane)].is_white == None):
                return False
        if not(isinstance(board[destination], Piece)):
            return True
        elif self.is_white and board[destination].is_white:
            return False
        elif not(self.is_white) and not(board[destination].is_white):
            return False
        return True

    def moves(self, board):
        result = set()
        i = 1
        while self.location[0]+i <= 7 and self.location[1]+i <=7:
            print('inside 1')
            if (piece:= board[self.location[0]+i, self.location[1]+i]) and piece.is_white is None:
                result.add(piece.location[0]*10 + piece.location[1])
                i += 1
            else:
                if (piece:= board[self.location[0]+i, self.location[1]+i]) and piece.is_white is not self.is_white:
                    result.add(piece.location[0]*10 + piece.location[1])
                break
        i = 1
        while self.location[0]+i <= 7 and self.location[1]-i >=0:
            print('inside 2')
            if (piece:= board[self.location[0]+i, self.location[1]-i]) and piece.is_white is None:
                result.add(piece.location[0]*10 + piece.location[1])
                i += 1
            else:
                if (piece:= board[self.location[0]+i, self.location[1]-i]) and piece.is_white is not self.is_white:
                    result.add(piece.location[0]*10 + piece.location[1])
                break
        i = 1
        while self.location[0]-i >= 0 and self.location[1]+i <=7:
            print('inside 3')
            piece= board[self.location[0]-i, self.location[1]+i]
            print(piece)
            print(piece.is_white)
            if (piece:= board[self.location[0]-i, self.location[1]+i]) and piece.is_white is None:

                result.add(piece.location[0]*10 + piece.location[1])
                i += 1
            else:
                if (piece:= board[self.location[0]-i, self.location[1]+i]) and piece.is_white is not self.is_white:
                    result.add(piece.location[0]*10 + piece.location[1])
                break
        i = 1
        while self.location[0]+i >=0 and self.location[1]-i >=0:
            print('inside 4')
            if (piece:= board[self.location[0]-i, self.location[1]-i]) and piece.is_white is None:
                result.add(piece.location[0]*10 + piece.location[1])
                i += 1
            else:
                if (piece:= board[self.location[0]-i, self.location[1]-i]) and piece.is_white is not self.is_white:
                    result.add(piece.location[0]*10 + piece.location[1])
                break
        print(result)
        return result

