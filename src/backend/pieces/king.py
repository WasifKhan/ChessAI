from io import DEFAULT_BUFFER_SIZE
from re import L
from .piece import Piece
from .pawn import Pawn
from .rook import Rook

class King(Piece):
    def __init__(self, ID, is_white, location):
        super().__init__(is_white, location)
        self.ID = ID
        self.value = 2

    def __str__(self):
        return 'K' if self.is_white else 'k'

    def _initialize_moves(self):
        direction = 1 if self.is_white else -1
        self.move_IDs[0] = lambda location: \
                (location[0]+1)*10 + location[1]+direction
        self.move_IDs[1] = lambda location: \
                (location[0]+1)*10 + location[1]
        self.move_IDs[2] = lambda location: \
                (location[0]+1)*10 + location[1]-direction
        self.move_IDs[3] = lambda location: \
                (location[0]-1)*10 + location[1]+direction
        self.move_IDs[4] = lambda location: \
                (location[0]-1)*10 + location[1]
        self.move_IDs[5] = lambda location: \
                (location[0]-1)*10 + location[1]-direction
        self.move_IDs[6] = lambda location: \
                location[0]*10 + location[1]+direction
        self.move_IDs[7] = lambda location: \
                location[0]*10 + location[1]-direction
        self.move_IDs[8] = lambda location: \
                (location[0]-2)*10 + location[1]
        self.move_IDs[9] = lambda location: \
                (location[0]+2)*10 + location[1]

    def _castle(self, board, destination):
        # Left Castle
        if self.location[0] - destination//10 == 2 and self.location[1] == destination%10:
            rook_location = destination//10-2, destination%10
            if isinstance(board[rook_location], Rook):
                for square in range(0,3):
                    for piece in (pieces := board.black_pieces if self.is_white else board.white_pieces):
                        if not isinstance(piece, King) and ((self.location[0] - square)*10 + self.location[1]) in piece.moves(board):
                            return False
                        if square >= 1 and board[(self.location[0] - square)*10 + self.location[1]].is_white is not None:
                            return False
                return True
        # Right Castle
        elif destination//10 - self.location[0] == 2 and self.location[1] == destination%10:
            rook_location = destination//10+1, destination%10
            if isinstance(board[rook_location], Rook):
                for square in range(0,3):
                    for piece in (pieces := board.black_pieces if self.is_white else board.white_pieces):
                        if not isinstance(piece, King) and ((self.location[0] + square)*10 + self.location[1]) in piece.moves(board):
                            return False
                        if square >= 1 and board[(self.location[0] + square)*10 + self.location[1]].is_white is not None:
                            return False
                return True

    def value(self):
        return 100

    def is_valid_move(self, board, destination):
        if self._castle(board, destination[0]*10 + destination[1]):
            return True
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
        if self._castle(board, (self.location[0]-2)*10 + self.location[1]):
            result.add((self.location[0]-2)*10 + self.location[1])
        elif self._castle(board, (self.location[0]+2)*10 + self.location[1]):
            result.add((self.location[0]+2)*10 + self.location[1])
        possible_location = {piece.location[0]*10 + piece.location[1] \
            for row in range(-1, 2) for col in range(-1, 2) if (row or col) \
            and (piece := board[self.location[0]+row, self.location[1]+col]) \
            and piece.is_white != self.is_white}
        opposing_attacks = set()
        for piece in (pieces := board.black_pieces if self.is_white else board.white_pieces):
            if isinstance(piece, Pawn):
                direction = 1 if piece.is_white else -1
                opposing_attacks.add((piece.location[0]+1)*10 + (piece.location[1]+direction))
                opposing_attacks.add((piece.location[0]-1)*10 + (piece.location[1]+direction))
            elif isinstance(piece, King):
                cells_around_king = {cell.location[0]*10 + cell.location[1] \
                    for row in range(-1, 2) for col in range(-1, 2) if (row or col) and (cell := board[piece.location[0]+row, piece.location[1]+col])}
                opposing_attacks |= cells_around_king
            else:
                opposing_attacks |= piece.moves(board)
        result = possible_location - opposing_attacks
        return result

    def checkmate(self, board):
        for enemy_piece in (enemy_pieces := board.black_pieces if self.is_white else board.white_pieces):
            if (self.location[0]*10 + self.location[1]) in enemy_piece.moves(board) \
                and self.moves(board) == set():
                captured = False
                for my_piece in (my_pieces := board.white_pieces if self.is_white else board.black_pieces):
                    if (enemy_piece.location[0]*10 + enemy_piece.location[1]) in my_piece.moves(board):
                        captured = True
                        break
                if not captured:
                    return True
        return False

