from .pieces.piece import Square, Piece
from .pieces.rook import Rook
from .pieces.knight import Knight
from .pieces.bishop import Bishop
from .pieces.queen import Queen
from .pieces.king import King
from .pieces.pawn import Pawn

class Board:
    def __init__(self, white_player='Player 1', black_player='Player 2'):
        self.white = white_player
        self.black = black_player
        self.history = []
        self.pieces = set()
        self.initialize_board()

    def __getitem__(self, key):
        if isinstance(key, tuple):
            return self.board[key[0]][key[1]]
        elif isinstance(key, int):
            return self.board[key//10][key%10]
        else:
            raise IndexError

    def __setitem__(self, key, val):
        if isinstance(key, tuple):
            self.board[key[0]][key[1]] = val
        elif isinstance(key, int):
            self.board[key] = val

    def __str__(self):
        output = ''
        for row in range(len(self.board) -1, -1, -1):
            for column in range(len(self.board)):
                output += f' {str(self.board[row][column])} '
            output += '\n'
        return output[0:-1]


    def initialize_board(self):
        board = [[Square(location=(y, x)) for y in range(8)] for x in range(8)]
        white_rook_1 = Rook(is_white=True, location=(0,0))
        white_rook_2 = Rook(is_white=True, location=(0,7))
        white_knight_1 = Knight(is_white=True, location=(0,1))
        white_knight_2 = Knight(is_white=True, location=(0,6))
        white_bishop_1 = Bishop(is_white=True, location=(0,2))
        white_bishop_2 = Bishop(is_white=True, location=(0,5))
        white_queen = Queen(is_white=True, location=(0,3))
        white_king = King(is_white=True, location=(0,4))
        white_pawn_1 = Pawn(is_white=True, location=(1,0))
        white_pawn_2 = Pawn(is_white=True, location=(1,1))
        white_pawn_3 = Pawn(is_white=True, location=(1,2))
        white_pawn_4 = Pawn(is_white=True, location=(1,3))
        white_pawn_5 = Pawn(is_white=True, location=(1,4))
        white_pawn_6 = Pawn(is_white=True, location=(1,5))
        white_pawn_7 = Pawn(is_white=True, location=(1,6))
        white_pawn_8 = Pawn(is_white=True, location=(1,7))
        black_rook_1 = Rook(is_white=False, location=(7,0))
        black_rook_2 = Rook(is_white=False, location=(7,7))
        black_knight_1 = Knight(is_white=False, location=(7,1))
        black_knight_2 = Knight(is_white=False, location=(7,6))
        black_bishop_1 = Bishop(is_white=False, location=(7,3))
        black_bishop_2 = Bishop(is_white=False, location=(7,5))
        black_queen = Queen(is_white=False, location=(7,3))
        black_king = King(is_white=False, location=(7,4))
        black_pawn_1 = Pawn(is_white=False, location=(6,0))
        black_pawn_2 = Pawn(is_white=False, location=(6,1))
        black_pawn_3 = Pawn(is_white=False, location=(6,2))
        black_pawn_4 = Pawn(is_white=False, location=(6,3))
        black_pawn_5 = Pawn(is_white=False, location=(6,4))
        black_pawn_6 = Pawn(is_white=False, location=(6,5))
        black_pawn_7 = Pawn(is_white=False, location=(6,6))
        black_pawn_8 = Pawn(is_white=False, location=(6,7))


        board[0][0] = white_rook_1
        self.pieces.add(white_rook_1)
        board[0][1] = white_knight_1
        self.pieces.add(white_knight_1)
        board[0][2] = white_bishop_1
        self.pieces.add(white_bishop_1)
        board[0][3] = white_queen
        self.pieces.add(white_queen)
        board[0][4] = white_king
        self.white_king = white_king
        self.pieces.add(white_king)
        board[0][5] = white_bishop_2
        self.pieces.add(white_bishop_2)
        board[0][6] = white_knight_2
        self.pieces.add(white_knight_2)
        board[0][7] = white_rook_2
        self.pieces.add(white_rook_2)
        board[1][0] = white_pawn_1
        self.pieces.add(white_pawn_1)
        board[1][1] = white_pawn_2
        self.pieces.add(white_pawn_2)
        board[1][2] = white_pawn_3
        self.pieces.add(white_pawn_3)
        board[1][3] = white_pawn_4
        self.pieces.add(white_pawn_4)
        board[1][4] = white_pawn_5
        self.pieces.add(white_pawn_5)
        board[1][5] = white_pawn_6
        self.pieces.add(white_pawn_6)
        board[1][6] = white_pawn_7
        self.pieces.add(white_pawn_7)
        board[1][7] = white_pawn_8
        self.pieces.add(white_pawn_8)
        board[6][0] = black_pawn_1
        self.pieces.add(black_pawn_1)
        board[6][1] = black_pawn_2
        self.pieces.add(black_pawn_2)
        board[6][2] = black_pawn_3
        self.pieces.add(black_pawn_3)
        board[6][3] = black_pawn_4
        self.pieces.add(black_pawn_4)
        board[6][4] = black_pawn_5
        self.pieces.add(black_pawn_5)
        board[6][5] = black_pawn_6
        self.pieces.add(black_pawn_6)
        board[6][6] = black_pawn_7
        self.pieces.add(black_pawn_7)
        board[6][7] = black_pawn_8
        self.pieces.add(black_pawn_8)
        board[7][0] = black_rook_1
        self.pieces.add(black_rook_1)
        board[7][1] = black_knight_1
        self.pieces.add(black_knight_1)
        board[7][2] = black_bishop_1
        self.pieces.add(black_bishop_1)
        board[7][3] = black_queen
        self.pieces.add(black_queen)
        board[7][4] = black_king
        self.black_king = black_king
        self.pieces.add(black_king)
        board[7][5] = black_bishop_2
        self.pieces.add(black_bishop_2)
        board[7][6] = black_knight_2
        self.pieces.add(black_knight_2)
        board[7][7] = black_rook_2
        self.pieces.add(black_rook_2)
        self.board = board


    def is_valid_move(self, piece, destination):
        return piece.is_valid_move(self.board, destination)


    def move(self, piece, destination):
        self.history.append((piece, piece.location, destination))

        # Update the board to move piece from previous location to destination
        previous_location = piece.location
        piece.location = destination
        captured_piece = self[destination]
        if (isinstance(captured_piece, Piece)):
            self.pieces.remove(captured_piece)
        self[destination] = piece
        self[previous_location] = Square(previous_location)
        # Edge case for en passant pawn capture
        if len(self.history) > 2:
            previous_move = self.history[-2]
            if (isinstance(previous_move[0], Pawn) and
                previous_move[1][1] - previous_move[2][1] == 2 and
                previous_move[2][0] == destination[0] and piece.location[1] == 5):
                    self[destination[0], destination[1] - 1] = Square((destination[0], destination[1] - 1))
            elif (isinstance(previous_move[0], Pawn) and
                previous_move[1][1] - previous_move[2][1] == -2 and
                previous_move[2][0] == destination[0] and piece.location[1] == 2):
                    self[(destination[0], destination[1] + 1)] = Square((destination[0], destination[1] + 1))

    def has_kings(self):
        return True if self.white_king in self.pieces and self.black_king in self.pieces else False


