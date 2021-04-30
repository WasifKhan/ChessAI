'''
Interface between backend and frontend
'''

from backend.game import Game
from frontend.view import View

class Interface:
    def __init__(self):
        # view = View()
        game = Game()
