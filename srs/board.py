from piece import Square, Rook, Knight, Bishop, Queen, King, Pawn

class Board:
    def __init__(self, white_player, black_player):
        self.white = white_player
        self.black = black_player
        self.board = initialize_board()      
        print('got here')

    def __str__(self):
        output = ''
        print('got hereee')
        for row in self.board:
            for col in row:
                print('got hereeeeeee')
                output += f'[{col.display()}]'
            output += '\n'
            print('got herefdsfsdfsd')
        return output


def initialize_board():
        board = [[Square(location=((x-1)*10 + y-1)) for x in range(8)] for y in range(8)]
        board[0][0] = Rook(is_white=True, location=0)
        board[0][1] = Knight(is_white=True, location=1)
        board[0][2] = Bishop(is_white=True, location=2)
        board[0][3] = Queen(is_white=True, location=3)
        board[0][4] = King(is_white=True, location=4)
        board[0][5] = Bishop(is_white=True, location=5)
        board[0][6] = Knight(is_white=True, location=6)
        board[0][7] = Rook(is_white=True, location=7)
        board[1][0] = Pawn(is_white=True, location=10)
        board[1][1] = Pawn(is_white=True, location=11)
        board[1][2] = Pawn(is_white=True, location=12)
        board[1][3] = Pawn(is_white=True, location=13)
        board[1][4] = Pawn(is_white=True, location=14)
        board[1][5] = Pawn(is_white=True, location=15)
        board[1][6] = Pawn(is_white=True, location=16)
        board[1][7] = Pawn(is_white=True, location=17)
        board[6][0] = Pawn(is_white=False, location=60)
        board[6][1] = Pawn(is_white=False, location=61)
        board[6][2] = Pawn(is_white=False, location=62)
        board[6][3] = Pawn(is_white=False, location=63)
        board[6][4] = Pawn(is_white=False, location=64)
        board[6][5] = Pawn(is_white=False, location=65)
        board[6][6] = Pawn(is_white=False, location=66)
        board[6][7] = Pawn(is_white=False, location=67)
        board[7][0] = Rook(is_white=False, location=70)
        board[7][1] = Knight(is_white=False, location=71)
        board[7][2] = Bishop(is_white=False, location=72)
        board[7][3] = Queen(is_white=False, location=73)
        board[7][4] = King(is_white=False, location=74)
        board[7][5] = Bishop(is_white=False, location=75)
        board[7][6] = Knight(is_white=False, location=76)
        board[7][7] = Rook(is_white=False, location=77)
        return board
