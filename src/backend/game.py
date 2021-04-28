'''
Class to simulate a game
'''

from .board import Board

class Game:
    def __init__(self, p1_name='Player 1', p2_name='Player 2'):
        self.player_1 = p1_name
        self.player_2 = p2_name
        self.board = Board()

    def add_move(self, move):
        pass

    def play_game(self, moves):
        pass

