'''
Class to simulate a game
'''

from .board import Board
from .pieces.king import King
from .scoreboard.scoreboard import Scoreboard


class Game:
    def __init__(self, p1_name='Player 1', p2_name='AI'):
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.board = Board()
        self.scoreboard = Scoreboard()
        self.white_turn = True

    def __str__(self):
        ret_val = '\n' + ('-'*24 + self.p2_name + '-'*24 + '\n')[0:54] + '\n'
        ret_val += str(self.board)
        ret_val += ('-'*24 + self.p1_name + '-'*24)[0:54]
        return ret_val

    def _add_games(self, player1, player2, p1_wins, p2_wins):
        self.scoreboard.add_games(player1, player2, p1_wins, p2_wins)

    def set_names(self, p1_name, p2_name):
        self.p1_name = p1_name
        self.p2_name = p2_name

    def move(self, source, destination):
        piece = self.board[source]
        destination = (destination//10, destination%10)
        # Execute move
        if piece.is_white is not None \
                and self.white_turn == piece.is_white \
                and self.board.is_valid_move(piece, destination):
            self.board.move(piece, destination)
            self.white_turn = not(self.white_turn)
            return True
        return False

    def is_game_over(self):
        return self.board.game_over

    def game_over(self, p1_wins, p2_wins):
        self._add_games(self.p1_name, self.p2_name, p1_wins, p2_wins)

    def get_scoreboard(self):
        return self.scoreboard.get_scoreboard()

    def get_score(self, player1, player2=None):
        return self.scoreboard.get_score(player1, player2)

    def reset_score(self, player1, player2=None):
        self.scoreboard.reset_score(player1, player2)
