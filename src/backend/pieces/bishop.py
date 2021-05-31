from .piece import Piece


class Bishop(Piece):
    def __init__(self, ID, is_white, location):
        super().__init__(is_white, location)
        self.ID = ID
        self.value = 3

    def __str__(self):
        return 'B' if self.is_white else 'b'

    def _initialize_moves(self):
        direction = 1 if self.is_white else -1
        self.move_IDs[0] = lambda location: \
                ((location[0]+7)%8)*10 + ((location[1]+7*direction)%8)
        self.move_IDs[1] = lambda location: \
                ((location[0]+6)%8)*10 + ((location[1]+6*direction)%8)
        self.move_IDs[2] = lambda location: \
                ((location[0]+5)%8)*10 + ((location[1]+5*direction)%8)
        self.move_IDs[3] = lambda location: \
                ((location[0]+4)%8)*10 + ((location[1]+4*direction)%8)
        self.move_IDs[4] = lambda location: \
                ((location[0]+3)%8)*10 + ((location[1]+3*direction)%8)
        self.move_IDs[5] = lambda location: \
                ((location[0]+2)%8)*10 + ((location[1]+2*direction)%8)
        self.move_IDs[6] = lambda location: \
                ((location[0]+1)%8)*10 + ((location[1]+1*direction)%8)
        self.move_IDs[7] = lambda location: \
                ((location[0]+7)%8)*10 + ((location[1]-7*direction)%8)
        self.move_IDs[8] = lambda location: \
                ((location[0]+6)%8)*10 + ((location[1]-6*direction)%8)
        self.move_IDs[9] = lambda location: \
                ((location[0]+5)%8)*10 + ((location[1]-5*direction)%8)
        self.move_IDs[10] = lambda location: \
                ((location[0]+4)%8)*10 + ((location[1]-4*direction)%8)
        self.move_IDs[11] = lambda location: \
                ((location[0]+3)%8)*10 + ((location[1]-3*direction)%8)
        self.move_IDs[12] = lambda location: \
                ((location[0]+2)%8)*10 + ((location[1]-2*direction)%8)
        self.move_IDs[13] = lambda location: \
                ((location[0]+1)%8)*10 + ((location[1]-1*direction)%8)

    def is_valid_move(self, board, destination):
        x_direction = destination[0] - self.location[0]
        y_direction = destination[1] - self.location[1]
        x_plane = 1 if x_direction > 0 else -1
        y_plane = 1 if y_direction > 0 else -1
        if abs(x_direction) != abs(y_direction):
            return False
        for i in range(1, abs(x_direction)):
            if not(board[self.location[0] + (i * x_plane),
                         self.location[1] + (i*y_plane)].is_white == None):
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
            if (piece:= board[self.location[0]+i, self.location[1]+i]) and piece.is_white is None:
                result.add(piece.location[0]*10 + piece.location[1])
                i += 1
            else:
                if (piece:= board[self.location[0]+i, self.location[1]+i]) and piece.is_white is not self.is_white:
                    result.add(piece.location[0]*10 + piece.location[1])
                break
        i = 1
        while self.location[0]+i <= 7 and self.location[1]-i >=0:
            if (piece:= board[self.location[0]+i, self.location[1]-i]) and piece.is_white is None:
                result.add(piece.location[0]*10 + piece.location[1])
                i += 1
            else:
                if (piece:= board[self.location[0]+i, self.location[1]-i]) and piece.is_white is not self.is_white:
                    result.add(piece.location[0]*10 + piece.location[1])
                break
        i = 1
        while self.location[0]-i >= 0 and self.location[1]+i <=7:
            piece= board[self.location[0]-i, self.location[1]+i]
            if (piece:= board[self.location[0]-i, self.location[1]+i]) and piece.is_white is None:

                result.add(piece.location[0]*10 + piece.location[1])
                i += 1
            else:
                if (piece:= board[self.location[0]-i, self.location[1]+i]) and piece.is_white is not self.is_white:
                    result.add(piece.location[0]*10 + piece.location[1])
                break
        i = 1
        while self.location[0]+i >=0 and self.location[1]-i >=0:
            if (piece:= board[self.location[0]-i, self.location[1]-i]) and piece.is_white is None:
                result.add(piece.location[0]*10 + piece.location[1])
                i += 1
            else:
                if (piece:= board[self.location[0]-i, self.location[1]-i]) and piece.is_white is not self.is_white:
                    result.add(piece.location[0]*10 + piece.location[1])
                break
        return result

