'''
Class to simulate a game
'''

from .board import Board



class Game:
    def __init__(self, p1_name='Player 1', p2_name='Player 2'):
        self.player_1 = p1_name
        self.player_2 = p2_name
        self.board = Board()
        self.play_game()


    def __str__(self):
        ret_val = '\n' + '=' * 30 + '\n'
        ret_val += str(self.board)
        ret_val += '=' * 30 + '\n'
        return ret_val


    def play_game(self):
        white_turn = True
        while self.board.has_kings():
            print(self)
            # Command format = <Origin> <Destination>
            # Origin = Destination = <Letter><Number>
            if white_turn:
                move = input('Enter white move: ')
            else:
                move = input('Enter black move: ')
            # Parse move
            origin = move.split(' ')[0]
            origin_x, origin_y = ord(origin[0]) - 65, int(origin[1]) - 1
            destination = move.split(' ')[1]
            destination_x, destination_y= ord(destination[0]) - 65, int(destination[1]) - 1
            piece = self.board[origin_x,origin_y]
            # Execute move
            if piece.is_white is not None and ((white_turn and piece.is_white) or (not(white_turn) and not(piece.is_white))) and piece.is_valid_move(self.board, (destination_x, destination_y)):
                self.board.move(piece, (destination_x, destination_y))
                white_turn = not(white_turn)
            else:
                print('invalid move, please enter a valid move')


