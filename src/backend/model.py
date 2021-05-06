'''
Class to simulate a game
'''

from .board import Board



class Game:
    def __init__(self):
        self.p1_name = 'Player 1'
        self.p2_name = 'AI'
        self.board = Board()
        self.white_turn = True

    def __str__(self):
        ret_val = '\n' + self.p2_name
        ret_val += '\n' + '-' * 23 + '\n'
        ret_val += str(self.board)
        ret_val += '\n' + '-' * 23 + '\n'
        ret_val += self.p1_name + '\n'
        return ret_val

    def set_names(self, p1_name, p2_name):
        self.p1_name = p1_name
        self.p2_name = p2_name


    def move(self, source, destination):
        piece = self.board[source]
        destination = (destination//10, destination%10)
        # Execute move
        if piece.is_white is not None \
                and ((self.white_turn and piece.is_white) or
                        (not(self.white_turn) and not(piece.is_white))) \
                and piece.is_valid_move(self.board, destination):
            self.board.move(piece, destination)
            self.white_turn = not(self.white_turn)
            return True
        return False

