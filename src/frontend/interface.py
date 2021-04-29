'''
Interface between backend and frontend
'''

from backend.game import Game

class Interface:
    def __init__(self):
        self.game = Game()
        self.game.play_game()
