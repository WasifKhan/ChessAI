from interface import Interface
from frontend.view import View
from backend.game import Game

if __name__ == '__main__':

    screen = View(Interface(Game()))


