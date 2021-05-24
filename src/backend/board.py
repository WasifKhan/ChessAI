from .pieces.piece import Square, Piece
from .pieces.rook import Rook
from .pieces.queen import Queen
from .pieces.king import King
from .pieces.pawn import Pawn

class Board:
    def __init__(self, pieces=None, history=None):
        from copy import copy
        self.history = []
        if history:
            for hist in history:
                self.history.append((copy(hist[0]), *hist[1:]))
        self.white_pieces = set()
        self.black_pieces = set()
        self.game_over = False
        self.board = [[Square(location=(x, y)) for y in range(8)] for x in range(8)]
        if not pieces:
            from .pieces.initial_pieces import PIECES as pieces
        for piece in pieces:
            self._add(copy(piece))

    def __str__(self):
        output = ''
        for row in range(len(self.board) -1, -1, -1):
            for column in range(len(self.board)):
                output += f' {str(self.board[column][row])} '
            output += '\n'
        return output[0:-1]

    def __copy__(self):
        return Board(self.white_pieces|self.black_pieces, self.history)

    def __getitem__(self, key):
        if isinstance(key, tuple):
            x, y = key[0], key[1]
        elif isinstance(key, int):
            x, y = key//10, key%10
        if x >= 0 and y >= 0 and x < len(self.board) and y < len(self.board[x]):
            return self.board[x][y]
        return None

    def __setitem__(self, key, val):
        if isinstance(key, tuple):
            x, y = key[0], key[1]
        elif isinstance(key, int):
            x, y=  key//10, key%10
        if x >= 0 and y >= 0 and x < 8 and y < 8:
            self.board[x][y] = val
        else:
            raise IndexError

    def is_valid_move(self, piece, destination):
        if self._check_after_move(piece, destination):
            return False
        return piece.is_valid_move(self, destination)

    def move(self, piece, destination):
        self.history.append((piece, piece.location, destination, self.board_value()))
        self._castle(piece, destination)
        self._enpassant(piece, destination)
        self._move_piece(piece, destination)
        self._promote(piece, destination)
        self._checkmate(piece, destination)

    def board_value(self):
        white_value = sum([piece.value for piece in self.white_pieces])
        black_value = sum([piece.value for piece in self.black_pieces])
        return white_value - black_value

    def _check_after_move(self, piece, destination):
        if (captured_piece := self[destination]).is_white == piece.is_white:
            return False
        self[destination] = piece
        self[piece.location] = Square(piece.location)
        if self._check(piece.is_white, captured_piece):
            self[piece.location] = piece
            self[destination] = captured_piece
            return True
        self[piece.location] = piece
        self[destination] = captured_piece
        return False

    def _check(self, is_white, excluded=None):
        king = self.white_king if is_white else self.black_king
        for piece in (pieces := self.black_pieces if is_white else self.white_pieces):
            if (king.location[0]*10 + king.location[1]) in piece.moves(self):
                if piece == excluded:
                    continue
                return True
        return False

    def _castle(self, piece, destination):
        if isinstance(piece, King):
            if piece.location[0] - destination[0] == 2:
                rook_location = destination[0]-2, destination[1]
                rook = self[rook_location]
                rook.move((piece.location[0]-1, piece.location[1]))
                self[piece.location[0]-1, piece.location[1]] = rook
                self[rook_location] = Square(rook_location)
            elif destination[0] - piece.location[0] == 2:
                rook_location = destination[0]+1, destination[1]
                rook = self[rook_location]
                rook.move((piece.location[0]+1, piece.location[1]))
                self[piece.location[0]+1, piece.location[1]] = rook
                self[rook_location] = Square(rook_location)

    def _enpassant(self, piece, destination):
        if isinstance(piece, Pawn):
            if destination[0] in {piece.location[0]-1, piece.location[0]+1} \
                    and self[destination].is_white == None:
                capture_location = destination[0], destination[1] - 1 if piece.is_white else destination[1] + 1
                capture_piece = self[capture_location]
                self.white_pieces.remove(capture_piece) \
                    if capture_piece.is_white \
                    else self.black_pieces.remove(capture_piece)
                self[capture_location] = Square(capture_location)

    def _promote(self, piece, destination):
        if isinstance(piece, Pawn):
            if piece.location[1] == 7 and piece.is_white:
                self.white_pieces.remove(piece)
                new_queen = Queen(is_white=True, location= piece.location)
                self.white_pieces.add(new_queen)
                self[piece.location] = new_queen
            elif piece.location[1] == 0 and not(piece.is_white):
                self.black_pieces.remove(piece)
                new_queen = Queen(is_white=False, location= piece.location)
                self.black_pieces.add(new_queen)
                self[piece.location] = new_queen

    def _checkmate(self, piece, destination):
        if (piece.is_white and self.black_king.checkmate(self)) \
                or (not(piece.is_white) and self.white_king.checkmate(self)):
            self.game_over = True

    def _move_piece(self, piece, destination):
        previous_location = piece.location
        piece.move(destination)
        ID = 1 if isinstance(piece, Queen) else piece.ID
        self.move_ID = str(piece) + str(ID) + str(piece.move_ID)
        captured_piece = self[destination]
        if (isinstance(captured_piece, Piece)):
            if captured_piece.is_white:
                self.white_pieces.remove(captured_piece)
            else:
                self.black_pieces.remove(captured_piece)
        self[destination] = piece
        self[previous_location] = Square(previous_location)

    def _add(self, piece):
        if piece.is_white:
            if isinstance(piece, King):
                self.white_king = piece
            self.white_pieces.add(piece)
        else:
            if isinstance(piece, King):
                self.black_king = piece
            self.black_pieces.add(piece)
        self[piece.location] = piece


