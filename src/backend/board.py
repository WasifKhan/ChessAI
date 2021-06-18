'''
Stores the logic for Chess board

Classes:
    Board
'''

from .pieces.piece import Square, Piece
from .pieces.rook import Rook
from .pieces.queen import Queen
from .pieces.king import King
from .pieces.pawn import Pawn
from .pieces.bishop import Bishop
from .pieces.knight import Knight



class Board:
    '''
    A class to represent a chess board

    ...
    Attributes
    ----------
    history: list
        list of previous moves to get to board state
    white_pieces: set(Piece)
        set of Piece classes for white pieces on board
    black_pieces: set(Piece)
        set of Piece classes for black pieces on board
    board: list(list(Piece))
        8x8 matrix containing Piece classes
    game_over: bool
        bool representing whether the game is over or not

    Methods
    -------
    print(Board): None
        prints the board in chess representation
    Board[location: int] -> Piece
        gets the Piece at the specified location
    Board[location: int] = piece: Piece -> None
        sets the board at the specified location to Piece
    is_valid_move(piece: Piece, destination: int) -> bool
        returns True if piece can move to destination
    move(piece: Piece, destination: int) -> None
        moves piece to destination
    board_value(): int
        returns the board value
    '''

    def __init__(self, pieces=None, history=None):
        '''
        Constructs all the necessary attributes for the board object

        Parameters
        ----------
            pieces: set(Piece)
                set of Pieces to be added to board
            history: list
                list of previous moves to get to current board state

        Returns
        -------
        None
        '''

        from copy import copy
        self.history = []
        if history:
            for hist in history:
                self.history.append((copy(hist[0]), *hist[1:]))
        self.white_pieces = set()
        self.black_pieces = set()
        self.game_over = False
        self.board = [[Square(location=(x, y), ID=x*10+y) for y in range(8)] for x in range(8)]
        if not pieces:
            from .pieces.initial_pieces import PIECES as pieces
        for piece in pieces:
            self._add_piece(copy(piece))


    def __str__(self):
        output = ''
        for row in range(len(self.board) -1, -1, -1):
            r1, r2, r3 = ['']*3
            for column in range(len(self.board)):
                out = '  ' + f'{str(self.board[column][row])}'*3 + '  '
                r1 += out
                r2 += out
                r3 += out
            output += f'{r1}\n{r2}\n{r3}\n\n\n'
        return output[0:-2]

    def __repr__(self):
        output = ''
        for row in range(8):
            for column in range(8):
                output += str(self.board[column][row])
        return output


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
        if not piece.is_valid_move(self, destination):
            return False
        return not self._check_after_move(piece, destination)


    def move(self, piece, destination):
        self.history.append((piece, piece.location, destination, self.value()))
        self._castle(piece, destination)
        self._move_piece(piece, destination)
        self._promote(piece, destination)
        self._checkmate(piece, destination)


    def value(self):
        white_value = sum([piece.value for piece in self.white_pieces])
        black_value = sum([piece.value for piece in self.black_pieces])
        return white_value - black_value


    def _check_after_move(self, piece, destination):
        if type(destination) == int:
            destination = (destination//10, destination%10)
        en_passant = None
        if isinstance(piece, Pawn) and piece.valid_en_passant(self, destination):
            en_passant = destination[0], destination[1] - 1 if piece.is_white else destination[1] + 1
        captured_piece = self[en_passant] if en_passant else self[destination]
        self[destination] = piece
        self[piece.location] = Square(piece.location,
                piece.location[0]*10+piece.location[1])
        if en_passant:
            self[en_passant] = Square(en_passant, en_passant[0]*10+en_passant[1])
        piece_location = piece.location
        piece.location = destination
        ret_val = self._check(piece.is_white, captured_piece)
        piece.location = piece_location
        self[piece.location] = piece
        if en_passant:
            self[en_passant] = captured_piece
            self[destination] = Square(destination, destination[0]*10+destination[1])
        else:
            self[destination] = captured_piece
        return ret_val


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
                self[rook_location] = Square(rook_location, rook_location[0]*10+rook_location[1])
            elif destination[0] - piece.location[0] == 2:
                rook_location = destination[0]+1, destination[1]
                rook = self[rook_location]
                rook.move((piece.location[0]+1, piece.location[1]))
                self[piece.location[0]+1, piece.location[1]] = rook
                self[rook_location] = Square(rook_location, rook_location[0]*10 + rook_location[1])


    def _promote(self, piece, destination):
        '''
        Minor bug - queen id should be incremented, not set to 2.
        Causes bugs if more than 2 white/black queens on board
        '''
        if isinstance(piece, Pawn):
            if piece.location[1] == 7 and piece.is_white:
                self.white_pieces.remove(piece)
                new_queen = Queen(2, is_white=True, location= piece.location)
                self.white_pieces.add(new_queen)
                self[piece.location] = new_queen
            elif piece.location[1] == 0 and not(piece.is_white):
                self.black_pieces.remove(piece)
                new_queen = Queen(2, is_white=False, location= piece.location)
                self.black_pieces.add(new_queen)
                self[piece.location] = new_queen


    def _checkmate(self, piece, destination):
        if (piece.is_white and self.black_king.checkmate(self)) \
                or (not(piece.is_white) and self.white_king.checkmate(self)):
            self.game_over = True


    def _move_piece(self, piece, destination):
        en_passant = None
        if isinstance(piece, Pawn) \
                and self[destination].is_white == None \
                and destination[0] != piece.location[0]:
            en_passant = destination[0], destination[1] - 1 if piece.is_white else destination[1] + 1
        previous_location = piece.location
        piece.move(destination)
        ID = 1 if isinstance(piece, Queen) else piece.ID
        self.move_ID = str(piece).upper() + str(ID) + str(piece.move_ID)
        captured_piece = self[en_passant] if en_passant else self[destination]
        if (isinstance(captured_piece, Piece)):
            if captured_piece.is_white:
                self.white_pieces.remove(captured_piece)
            else:
                self.black_pieces.remove(captured_piece)
        self[destination] = piece
        self[previous_location] = Square(previous_location, previous_location[0]*10 + previous_location[1])
        if en_passant:
            self[en_passant] = Square(en_passant, en_passant[0]*10+en_passant[1])


    def _add_piece(self, piece):
        if piece.is_white:
            if isinstance(piece, King):
                self.white_king = piece
            self.white_pieces.add(piece)
        else:
            if isinstance(piece, King):
                self.black_king = piece
            self.black_pieces.add(piece)
        self[piece.location] = piece

