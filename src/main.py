if __name__ == '__main__':
    from interface import Interface
    from frontend.view import View
    from backend.model import Game

    View(Interface(Game()))
