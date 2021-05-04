'''
Class to simulate a game
'''

from .board import Board



class Game:
    def __init__(self, p1_name='Player 1', p2_name='Player 2'):
        self.player_1 = p1_name
        self.player_2 = p2_name
        self.board = Board()
        self.white_turn = True

    def __str__(self):
        ret_val = '\n' + '=' * 30 + '\n'
        ret_val += str(self.board)
        ret_val += '\n' + '=' * 30 + '\n'
        return ret_val


    def move(self, source, destination):
        piece = self.board[source]
        destination = (destination//10, destination%10)
        print(destination)
        # Execute move
        if piece.is_white is not None \
                and ((self.white_turn and piece.is_white) or
                        (not(self.white_turn) and not(piece.is_white))) \
                and piece.is_valid_move(self.board, destination):
            self.board.move(piece, destination)
            self.white_turn = not(self.white_turn)
            return True

        else:
            print('invalid move, please enter a valid move')
            return False

