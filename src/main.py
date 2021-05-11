if __name__ == '__main__':
    from interface import Interface
    from frontend.view import View
    from backend.game import Game
    from ai.ai import AI

    View(Interface(Game(), AI(1)))
