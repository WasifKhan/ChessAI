from .piece import Square, Rook, Knight, Bishop, Queen, King, Pawn

class Board:
    def __init__(self, white_player='Player 1', black_player='Player 2'):
        self.white = white_player
        self.black = black_player
        self.history = []
        self.pieces = {'$': set(),
                        'Q': set(),
                        'R': set(),
                        'K': set(),
                        'B': set(),
                        'P': set(),
                        '-': set(),
                        'q': set(),
                        'r': set(),
                        'k': set(),
                        'b': set(),
                        'p': set()
        }
        self.initialize_board()
    def __getitem__(self, key):
        if isinstance(key, tuple):
            return self.board[key[0]][key[1]]
        elif isinstance(key, int):
            return self.board[key]

    def __setitem__(self, key, val):
        self.board[key] = val

    def __str__(self):
        output = ''
        for column in range(len(self.board) -1, -1, -1):
            for row in range(len(self.board)):
                output += f' {str(self.board[row][column])} '
            output += '\n'
        return output[0:-1]


    def initialize_board(self):
        board = [[Square(location=((x-1)*10, y-1)) for x in range(8)] for y in range(8)]
        board[0][0] = Rook(is_white=True, location=(0,0))
        self.pieces['R'].add(0)
        board[1][0] = Knight(is_white=True, location=(1,0))
        self.pieces['K'].add(10)
        board[2][0] = Bishop(is_white=True, location=(2,0))
        self.pieces['B'].add(20)
        board[3][0] = Queen(is_white=True, location=(3,0))
        self.pieces['Q'].add(30)
        board[4][0] = King(is_white=True, location=(4,0))
        self.white_king_location = (4, 0)
        self.pieces['$'].add(40)
        board[5][0] = Bishop(is_white=True, location=(5,0))
        self.pieces['B'].add(50)
        board[6][0] = Knight(is_white=True, location=(6,0))
        self.pieces['K'].add(60)
        board[7][0] = Rook(is_white=True, location=(7,0))
        self.pieces['R'].add(70)
        board[0][1] = Pawn(is_white=True, location=(0,1)) 
        [self.pieces['P'].add((i*10 +1) for i in range(8))]
        board[1][1] = Pawn(is_white=True, location=(1,1))
        board[2][1] = Pawn(is_white=True, location=(2,1))
        board[3][1] = Pawn(is_white=True, location=(3,1))
        board[4][1] = Pawn(is_white=True, location=(4,1))
        board[5][1] = Pawn(is_white=True, location=(5,1))
        board[6][1] = Pawn(is_white=True, location=(6,1))
        board[7][1] = Pawn(is_white=True, location=(7,1))
        [self.pieces['p'].add((i*10 +6) for i in range((8)))]
        board[0][6] = Pawn(is_white=False, location=(0,6))
        board[1][6] = Pawn(is_white=False, location=(1,6))
        board[2][6] = Pawn(is_white=False, location=(2,6))
        board[3][6] = Pawn(is_white=False, location=(3,6))
        board[4][6] = Pawn(is_white=False, location=(4,6))
        board[5][6] = Pawn(is_white=False, location=(5,6))
        board[6][6] = Pawn(is_white=False, location=(6,6))
        board[7][6] = Pawn(is_white=False, location=(7,6))
        board[0][7] = Rook(is_white=False, location=(0,7))
        self.pieces['r'].add(7)
        board[1][7] = Knight(is_white=False, location=(1,7))
        self.pieces['k'].add(17)
        board[2][7] = Bishop(is_white=False, location=(2,7))
        self.pieces['b'].add(27)
        board[3][7] = Queen(is_white=False, location=(3,7))
        self.pieces['q'].add(37)
        board[4][7] = King(is_white=False, location=(4,7))
        self.black_king_location = (4, 7)
        self.pieces['-'].add(47)
        board[5][7] = Bishop(is_white=False, location=(5,7))
        self.pieces['b'].add(57)
        board[6][7] = Knight(is_white=False, location=(6,7))
        self.pieces['k'].add(67)
        board[7][7] = Rook(is_white=False, location=(7,7))
        self.pieces['r'].add(77)
        self.board = board


    def is_valid_move(self, piece, destination):
        return piece.is_valid_move(self.board, destination)


    def move(self, piece, destination):
        # Edge-case King check
        if isinstance(piece, King):
            if piece.is_white:
                self.white_king_location = destination
            else:
                self.black_king_location = destination
        if isinstance(self.board[destination[0]][destination[1]], King):
            if self.board[destination[0]][destination[1]].is_white:
                self.white_king_location = None
            else:
                self.black_king_location = None

        self.history.append((piece, piece.location, destination))

        # Update the board to move piece from previous location to destination
        previous_location = piece.location
        piece.location = destination
        old_piece = str(self.board[destination[0]][destination[1]])
        if old_piece != '-':
            self.pieces[piece].remove(previous_location[0]*10 + previous_location[1])
        self.pieces[str(piece)].remove(previous_location[0]*10 + previous_location[1])
        self.pieces[str(piece)].add(destination[0]*10 + destination[1])
        self.board[destination[0]][destination[1]] = piece
        self.board[previous_location[0]][previous_location[1]] = Square(previous_location)
        # Edge case for en passant pawn capture
        if len(self.history) > 2:
            previous_move = self.history[-2]
            if (isinstance(previous_move[0], Pawn) and
                previous_move[1][1] - previous_move[2][1] == 2 and
                previous_move[2][0] == destination[0] and piece.location[1] == 5):
                    self.board[destination[0]][destination[1] - 1] = Square((destination[0], destination[1] - 1))
            elif (isinstance(previous_move[0], Pawn) and
                previous_move[1][1] - previous_move[2][1] == -2 and
                previous_move[2][0] == destination[0] and piece.location[1] == 2):
                    self.board[destination[0]][destination[1] + 1] = Square((destination[0], destination[1] + 1))

    def has_kings(self):
        return True if self.white_king_location and self.black_king_location else False


