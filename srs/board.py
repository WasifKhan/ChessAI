from piece import Square, Rook, Knight, Bishop, Queen, King, Pawn

class Board:
    def __init__(self):
        self.board = [[Square(location=((x-1)*10 + y-1)) for x in range(8)] for y in range(8)]
        self.board[0][0] = Rook(is_white=True, location=0)
        self.board[0][1] = Knight(is_white=True, location=1)
        self.board[0][2] = Bishop(is_white=True, location=2)
        self.board[0][3] = Queen(is_white=True, location=3)
        self.board[0][4] = King(is_white=True, location=4)
        self.board[0][5] = Bishop(is_white=True, location=5)
        self.board[0][6] = Knight(is_white=True, location=6)
        self.board[0][7] = Rook(is_white=True, location=7)
        self.board[1][0] = Pawn(is_white=True, location=10)
        self.board[1][1] = Pawn(is_white=True, location=11)
        self.board[1][2] = Pawn(is_white=True, location=12)
        self.board[1][3] = Pawn(is_white=True, location=13)
        self.board[1][4] = Pawn(is_white=True, location=14)
        self.board[1][5] = Pawn(is_white=True, location=15)
        self.board[1][6] = Pawn(is_white=True, location=16)
        self.board[1][7] = Pawn(is_white=True, location=17)
        self.board[6][0] = Pawn(is_white=False, location=60)
        self.board[6][1] = Pawn(is_white=False, location=61)
        self.board[6][2] = Pawn(is_white=False, location=62)
        self.board[6][3] = Pawn(is_white=False, location=63)
        self.board[6][4] = Pawn(is_white=False, location=64)
        self.board[6][5] = Pawn(is_white=False, location=65)
        self.board[6][6] = Pawn(is_white=False, location=66)
        self.board[6][7] = Pawn(is_white=False, location=67)
        self.board[7][0] = Rook(is_white=False, location=70)
        self.board[7][1] = Knight(is_white=False, location=71)
        self.board[7][2] = Bishop(is_white=False, location=72)
        self.board[7][3] = Queen(is_white=False, location=73)
        self.board[7][4] = King(is_white=False, location=74)
        self.board[7][5] = Bishop(is_white=False, location=75)
        self.board[7][6] = Knight(is_white=False, location=76)
        self.board[7][7] = Rook(is_white=False, location=77)
        


    def __str__(self):
        output = ''
        for x in range(len(self.board)):
            output += str(self.board[x])
            output += '\n'
        return output