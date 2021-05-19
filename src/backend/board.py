from .pieces.piece import Square, Piece
from .pieces.rook import Rook
from .pieces.knight import Knight
from .pieces.bishop import Bishop
from .pieces.queen import Queen
from .pieces.king import King
from .pieces.pawn import Pawn

class Board:
    def __init__(self, pieces=None, history=None):
        self.history = []
        if history:
            self.history = history
        self.white_pieces = set()
        self.black_pieces = set()
        self.game_over = False
        self._initialize_board(pieces)

    def __str__(self):
        output = ''
        for row in range(len(self.board) -1, -1, -1):
            for column in range(len(self.board)):
                output += f' {str(self.board[column][row])} '
            output += '\n'
        return output[0:-1]

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

    def __deepcopy__(self, memo):
        from copy import deepcopy
        return Board(deepcopy(self.white_pieces | self.black_pieces), deepcopy(self.history))

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

    def board_value(self):
        white_value = sum([piece.value for piece in self.white_pieces])
        black_value = sum([piece.value for piece in self.black_pieces])
        return white_value - black_value

    def check(self, is_white):
        king = self.white_king if is_white else self.black_king
        for piece in (pieces := self.black_pieces if is_white else self.white_pieces):
            if (king.location[0]*10 + king.location[1]) in piece.moves(self):
                return True
        return False

    def move(self, piece, destination):
        self.history.append((piece, piece.location, destination, self.board_value()))
        # Edge case for castling
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
        # Edge case for en passant pawn capture
        if len(self.history) > 3:
            previous_move = self.history[-2]
            if isinstance(piece, Pawn) \
                and isinstance(previous_move[0], Pawn) \
                and previous_move[1][1] - previous_move[2][1] == 2 \
                and previous_move[2][0] == destination[0] and piece.location[1] == 4 \
                and destination[0] in {piece.location[0]-1, piece.location[0]+1}:
                    capture_location = destination[0], destination[1] - 1
                    capture_piece = self[capture_location]
                    self.black_pieces.remove(capture_piece)
                    self[capture_location] = Square(capture_location)
            elif isinstance(piece, Pawn) \
                and isinstance(previous_move[0], Pawn) \
                and previous_move[1][1] - previous_move[2][1] == -2 \
                and previous_move[2][0] == destination[0] and piece.location[1] == 3 \
                and destination[0] in {piece.location[0]-1, piece.location[0]+1}:
                    capture_location = destination[0], destination[1] + 1
                    capture_piece = self[capture_location]
                    self.white_pieces.remove(capture_piece)
                    self[capture_location] = Square(capture_location)
        # Update the board to move piece from previous location to destination
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
        # Check for promotion
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


        # Check if the move resulted in checkmate
        if (piece.is_white and self.black_king.checkmate(self)) \
                or (not(piece.is_white) and self.white_king.checkmate(self)):
            self.game_over = True

    def _initialize_board(self, pieces):
        board = [[Square(location=(x, y)) for y in range(8)] for x in range(8)]
        if pieces:
            from copy import deepcopy
            self.board = deepcopy(board)
            for piece in pieces:
                self._add(piece)
            return
        white_rook_1 = Rook(is_white=True, location=(0,0))
        white_rook_2 = Rook(is_white=True, location=(7,0))
        white_knight_1 = Knight(is_white=True, location=(1,0))
        white_knight_2 = Knight(is_white=True, location=(6,0))
        white_bishop_1 = Bishop(is_white=True, location=(2,0))
        white_bishop_2 = Bishop(is_white=True, location=(5,0))
        white_queen = Queen(is_white=True, location=(3,0))
        white_king = King(is_white=True, location=(4,0))
        white_pawn_1 = Pawn(is_white=True, location=(0,1))
        white_pawn_2 = Pawn(is_white=True, location=(1,1))
        white_pawn_3 = Pawn(is_white=True, location=(2,1))
        white_pawn_4 = Pawn(is_white=True, location=(3,1))
        white_pawn_5 = Pawn(is_white=True, location=(4,1))
        white_pawn_6 = Pawn(is_white=True, location=(5,1))
        white_pawn_7 = Pawn(is_white=True, location=(6,1))
        white_pawn_8 = Pawn(is_white=True, location=(7,1))
        black_rook_1 = Rook(is_white=False, location=(0,7))
        black_rook_2 = Rook(is_white=False, location=(7,7))
        black_knight_1 = Knight(is_white=False, location=(1,7))
        black_knight_2 = Knight(is_white=False, location=(6,7))
        black_bishop_1 = Bishop(is_white=False, location=(2,7))
        black_bishop_2 = Bishop(is_white=False, location=(5,7))
        black_queen = Queen(is_white=False, location=(3,7))
        black_king = King(is_white=False, location=(4,7))
        black_pawn_1 = Pawn(is_white=False, location=(0,6))
        black_pawn_2 = Pawn(is_white=False, location=(1,6))
        black_pawn_3 = Pawn(is_white=False, location=(2,6))
        black_pawn_4 = Pawn(is_white=False, location=(3,6))
        black_pawn_5 = Pawn(is_white=False, location=(4,6))
        black_pawn_6 = Pawn(is_white=False, location=(5,6))
        black_pawn_7 = Pawn(is_white=False, location=(6,6))
        black_pawn_8 = Pawn(is_white=False, location=(7,6))


        board[0][0] = white_rook_1
        self.white_pieces.add(white_rook_1)
        board[1][0] = white_knight_1
        self.white_pieces.add(white_knight_1)
        board[2][0] = white_bishop_1
        self.white_pieces.add(white_bishop_1)
        board[3][0] = white_queen
        self.white_pieces.add(white_queen)
        board[4][0] = white_king
        self.white_king = white_king
        self.white_pieces.add(white_king)
        board[5][0] = white_bishop_2
        self.white_pieces.add(white_bishop_2)
        board[6][0] = white_knight_2
        self.white_pieces.add(white_knight_2)
        board[7][0] = white_rook_2
        self.white_pieces.add(white_rook_2)
        board[0][1] = white_pawn_1
        self.white_pieces.add(white_pawn_1)
        board[1][1] = white_pawn_2
        self.white_pieces.add(white_pawn_2)
        board[2][1] = white_pawn_3
        self.white_pieces.add(white_pawn_3)
        board[3][1] = white_pawn_4
        self.white_pieces.add(white_pawn_4)
        board[4][1] = white_pawn_5
        self.white_pieces.add(white_pawn_5)
        board[5][1] = white_pawn_6
        self.white_pieces.add(white_pawn_6)
        board[6][1] = white_pawn_7
        self.white_pieces.add(white_pawn_7)
        board[7][1] = white_pawn_8
        self.white_pieces.add(white_pawn_8)
        board[0][6] = black_pawn_1
        self.black_pieces.add(black_pawn_1)
        board[1][6] = black_pawn_2
        self.black_pieces.add(black_pawn_2)
        board[2][6] = black_pawn_3
        self.black_pieces.add(black_pawn_3)
        board[3][6] = black_pawn_4
        self.black_pieces.add(black_pawn_4)
        board[4][6] = black_pawn_5
        self.black_pieces.add(black_pawn_5)
        board[5][6] = black_pawn_6
        self.black_pieces.add(black_pawn_6)
        board[6][6] = black_pawn_7
        self.black_pieces.add(black_pawn_7)
        board[7][6] = black_pawn_8
        self.black_pieces.add(black_pawn_8)
        board[0][7] = black_rook_1
        self.black_pieces.add(black_rook_1)
        board[1][7] = black_knight_1
        self.black_pieces.add(black_knight_1)
        board[2][7] = black_bishop_1
        self.black_pieces.add(black_bishop_1)
        board[3][7] = black_queen
        self.black_pieces.add(black_queen)
        board[4][7] = black_king
        self.black_king = black_king
        self.black_pieces.add(black_king)
        board[5][7] = black_bishop_2
        self.black_pieces.add(black_bishop_2)
        board[6][7] = black_knight_2
        self.black_pieces.add(black_knight_2)
        board[7][7] = black_rook_2
        self.black_pieces.add(black_rook_2)
        self.board = board

