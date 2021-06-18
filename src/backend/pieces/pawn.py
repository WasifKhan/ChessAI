from .piece import Piece


class Pawn(Piece):
    def __init__(self, ID, is_white, location):
        super().__init__(is_white, location)
        self.ID = ID
        self.value = 1

    def __str__(self):
        return 'P' if self.is_white else 'p'

    def _initialize_moves(self):
        direction = 1 if self.is_white else -1
        self.move_IDs[0] = lambda location: \
                location[0]*10 + location[1] + direction
        self.move_IDs[1] = lambda location: \
                location[0]*10 + location[1] + (direction * 2)
        self.move_IDs[2] = lambda location: \
                (location[0] - 1)*10 + (location[1] + direction)
        self.move_IDs[3] = lambda location: \
                (location[0] + 1)*10 + (location[1] + direction)

    def _defends(self, board):
        direction = 1 if self.is_white else -1
        their_pieces = board.black_pieces if self.is_white else board.white_pieces
        values = []
        piece_1 = board[self.location[0]-1, self.location[1]+direction]
        piece_2 = board[self.location[0]+1, self.location[1]+direction]
        if piece_1 and piece_1.is_white == self.is_white and piece_1.value != 2:
            location = piece_1.location[0]*10 + piece_1.location[1]
            for piece in their_pieces:
                if location in piece.moves(board):
                    values.append(piece_1.value)
        if piece_2 and piece_2.is_white == self.is_white and piece_2.value != 2:
            location = piece_2.location[0]*10 + piece_2.location[1]
            for piece in their_pieces:
                if location in piece.moves(board):
                    values.append(piece_2.value)
        return values

    def valid_en_passant(self, board, destination):
        y_movement = 2 if self.is_white else -2
        location = 4 if self.is_white else 3
        if board.history:
            previous_move = board.history[-1]
            if (isinstance(previous_move[0], Pawn) \
                    and previous_move[1][1] - previous_move[2][1] == y_movement \
                    and previous_move[2][0] == destination[0] \
                    and self.location[1] == location):
                return True
        return False


    def is_valid_move(self, board, destination):
        if self.is_white:
            # Check for diagonal movement
            if (self.location[1] + 1 == destination[1] and
               (self.location[0] + 1 == destination[0] or
                self.location[0] - 1 == destination[0])):
                if board[destination].is_white == False:
                    return True
                # Check for en passant movement
                if self.valid_en_passant(board, destination):
                    return True
            # Check for vertical movement - 1 square
            if (self.location[1] + 1 == destination[1] and
                self.location[0] == destination[0]):
                if board[destination].is_white == None:
                    return True
            # Check for vertical movement - 2 squares
            elif (self.location[1] + 2 == destination[1] \
                    and self.location[0] == destination[0] \
                    and self.location[1] == 1):
                if (board[destination].is_white == None and
                    board[(destination[0], destination[1] - 1)].is_white == None):
                    return True
        else:
            # Check for diagonal movement
            if self.location[1] - 1 == destination[1] \
                and (self.location[0] + 1 == destination[0] \
                    or self.location[0] - 1 == destination[0]):
                if board[destination].is_white:
                    return True
                if self.valid_en_passant(board, destination):
                    return True
            # Check for vertical movement - 1 square
            if (self.location[1] - 1 == destination[1] and
                self.location[0] == destination[0]):
                if board[destination].is_white == None:
                    return True
            # Check for vertical movement - 2 squares
            elif (self.location[1] - 2 == destination[1] and
                  self.location[0] == destination[0] and
                  self.location[1] == 6):
                if (board[destination].is_white == None and
                    board[(destination[0], destination[1] + 1)].is_white == None):
                    return True
        return False

    def moves(self, board):
        result = set()
        y_direction = 1 if self.is_white else -1
        # Single vertical movement
        if (piece:= board[self.location[0], self.location[1] + y_direction]) is not None and piece.is_white is None:
            result.add(piece.location[0] * 10 + piece.location[1])
        # Double vertical movement
        if (self.location[1] == 1 and self.is_white) or (self.location[1] == 6 and not(self.is_white)):
            if board[self.location[0], self.location[1] + y_direction].is_white is None \
                    and (piece:= board[self.location[0], self.location[1] + y_direction * 2]).is_white is None:
                result.add(piece.location[0] * 10 + piece.location[1])
        # Capture
        if (self.location[0] == 0):
            if (piece:= board[self.location[0] + 1, self.location[1] + y_direction]) is not None \
                and piece.is_white is not None \
                and piece.is_white is not self.is_white:
                result.add(piece.location[0] * 10 + piece.location[1])
        elif (self.location[0] == 7):
            if (piece:= board[self.location[0] - 1, self.location[1] + y_direction]) is not None \
                and piece.is_white is not None \
                and piece.is_white is not self.is_white:
                result.add(piece.location[0] * 10 + piece.location[1])
        else:
            if (piece:= board[self.location[0] + 1, self.location[1] + y_direction]) is not None \
                and piece.is_white is not None \
                and piece.is_white is not self.is_white:
                result.add(piece.location[0] * 10 + piece.location[1])
            if (piece:= board[self.location[0] - 1, self.location[1] +
                y_direction]) is not None \
                and piece.is_white is not None \
                and piece.is_white is not self.is_white:
                result.add(piece.location[0] * 10 + piece.location[1])
        # En passant
        if board.history:
            if self.location[1] == 3 and isinstance(board[self.location[0]-1, self.location[1]], Pawn) and \
                board[self.location[0]-1, self.location[1]].is_white is not self.is_white:
                    previous_move = board.history[-1]
                    if isinstance(previous_move[0], Pawn) and previous_move[1][1] - previous_move[2][1] == -2 and\
                        previous_move[2][0] == self.location[0] - 1:
                        result.add((self.location[0]-1)*10 + self.location[1]-1)

            if self.location[1] == 3 and isinstance(board[self.location[0]+1, self.location[1]], Pawn) and \
                board[self.location[0]+1, self.location[1]].is_white is not self.is_white:
                    previous_move = board.history[-1]
                    if isinstance(previous_move[0], Pawn) and previous_move[1][1] - previous_move[2][1] == -2 and\
                        previous_move[2][0] == self.location[0] + 1:
                        result.add((self.location[0]+1)*10 + self.location[1]-1)
            if self.location[1] == 4 and isinstance(board[self.location[0]-1, self.location[1]], Pawn) and \
                board[self.location[0]-1, self.location[1]].is_white is not self.is_white:
                    previous_move = board.history[-1]
                    if isinstance(previous_move[0], Pawn) and previous_move[1][1] - previous_move[2][1] == -2 and\
                        previous_move[2][0] == self.location[0] - 1:
                        result.add((self.location[0]-1)*10 + self.location[1]+1)
            if self.location[1] == 4 and isinstance(board[self.location[0]+1, self.location[1]], Pawn) and \
                board[self.location[0]+1, self.location[1]].is_white is not self.is_white:
                    previous_move = board.history[-1]
                    if isinstance(previous_move[0], Pawn) and previous_move[1][1] - previous_move[2][1] == -2 and\
                        previous_move[2][0] == self.location[0] + 1:
                        result.add((self.location[0]+1)*10 + self.location[1]+1)
        return result

