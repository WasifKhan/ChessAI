'''
Interface between backend and frontend
'''

class Interface:
    def __init__(self, game):
        self.game = game
        self.current_move = None
        print(game)

    def __str__(self):
        return str(self.game)

    def add_action(self, location):
        if (source := self.current_move) is not None:
            self.game.move(source, location)
            self.current_move = None
            print(f'move: {source} -> {location}')
            print(self.game)
        else:
            self.current_move = location

