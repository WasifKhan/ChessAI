'''
Interface between backend and frontend
'''

from backend.game import Game
from ai.ai import AI

class Interface:
    def __init__(self, player_1='Player1', player_2='Player 2'):
        self.game = Game(player_1, player_2)
        self.current_move = None
        self.AI = None
        print(self.game)

    def __str__(self):
        return str(self.game)

    def versus_AI(self, difficulty=0):
        self.AI = AI(0)

    def add_action(self, location):
        if (source := self.current_move) is not None:
            if self.game.move(source, location):
                self.current_move = None
                print(f'move: {source} -> {location}')
                print(self.game)
            if self.AI:
                source, location = self.AI.get_move(self.game.board)
                if self.game.move(source, location):
                    print(f'AI move: {source} -> {location}')
                    print(self.game)
        else:
            self.current_move = location


    def set_game_type(self, human=False):
        return True

    def set_player_name(self, player_1='Player 1', player_2='Player 2'):
        return True

    def add_move(self, source, destination):
        return True

    def get_scoreboard(self):
        return True

    def get_score(self, player1, player2=None):
        return True

    def game_over(self):
        return False

    def play_again(self, yes=True):
        return True
