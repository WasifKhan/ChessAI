from piece import Square, Rook, Knight, Bishop, Queen, King, Pawn

class Board:
    def __init__(self, white_player, black_player):
        self.white = white_player
        self.black = black_player
        self.initialize_board()

    def initialize_board(self):
        board = [[Square(location=((x-1)*10, y-1)) for x in range(8)] for y in range(8)]
        board[0][0] = Rook(is_white=True, location=(0,0))
        board[0][1] = Knight(is_white=True, location=(0,1))
        board[0][2] = Bishop(is_white=True, location=(0,2))
        board[0][3] = Queen(is_white=True, location=(0,3))
        board[0][4] = King(is_white=True, location=(0,4))
        self.white_king_location = (0, 4)
        board[0][5] = Bishop(is_white=True, location=(0,5))
        board[0][6] = Knight(is_white=True, location=(0,6))
        board[0][7] = Rook(is_white=True, location=(0,7))
        board[1][0] = Pawn(is_white=True, location=(1,0))
        board[1][1] = Pawn(is_white=True, location=(1,1))
        board[1][2] = Pawn(is_white=True, location=(1,2))
        board[1][3] = Pawn(is_white=True, location=(1,3))
        board[1][4] = Pawn(is_white=True, location=(1,4))
        board[1][5] = Pawn(is_white=True, location=(1,5))
        board[1][6] = Pawn(is_white=True, location=(1,6))
        board[1][7] = Pawn(is_white=True, location=(1,7))
        board[6][0] = Pawn(is_white=False, location=(6,0))
        board[6][1] = Pawn(is_white=False, location=(6,1))
        board[6][2] = Pawn(is_white=False, location=(6,2))
        board[6][3] = Pawn(is_white=False, location=(6,3))
        board[6][4] = Pawn(is_white=False, location=(6,4))
        board[6][5] = Pawn(is_white=False, location=(6,5))
        board[6][6] = Pawn(is_white=False, location=(6,6))
        board[6][7] = Pawn(is_white=False, location=(6,7))
        board[7][0] = Rook(is_white=False, location=(7,0))
        board[7][1] = Knight(is_white=False, location=(7,1))
        board[7][2] = Bishop(is_white=False, location=(7,2))
        board[7][3] = Queen(is_white=False, location=(7,3))
        board[7][4] = King(is_white=False, location=(7,4))
        self.black_king_location = (7, 4)
        board[7][5] = Bishop(is_white=False, location=(7,5))
        board[7][6] = Knight(is_white=False, location=(7,6))
        board[7][7] = Rook(is_white=False, location=(7,7))
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

        # Update the board to move piece from previous location to destination
        previous_location = piece.location
        piece.location = destination
        self.board[destination[0]][destination[1]] = piece 
        self.board[previous_location[0]][previous_location[1]] = Square(previous_location)


    def has_kings(self):
        return True if self.white_king_location and self.black_king_location else False
        
        self.board = initialize_board()      
        print('got here')

    def __str__(self):
        output = ''
        for row in range(len(self.board) -1, -1, -1):
            for col in self.board[row]:
                output += f'[{col.display()}]'
            output += '\n'
        return output

