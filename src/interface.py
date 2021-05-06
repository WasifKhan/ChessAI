'''
Interface between backend and frontend
'''

from ai.ai import AI



class Interface:
    def __init__(self, game):
        self.game = game
        self.AI = None
        print(self.game)

    def __str__(self):
        return str(self.game)

    def versus_AI(self, difficulty=0):
        self.AI = AI(difficulty)

    def set_player_names(self, p1_name='Player 1', p2_name='AI'):
        self.game.set_names(p1_name, p2_name)

    def game_over(self, root):
        print('*'*30)
        if not self.game.is_game_over():
            if self.game.white_turn:
                print('*' * 7 + f'{self.game.p1_name} resigned' + '*' * 6)
            else:
                print(f'{self.game.p2_name} resigned')

        print('*'*30)
        print('*'*11 + 'GAME OVER' + '*'*10)
        print('*'*30)
        self.game.game_over()
        root.destroy()

    def add_move(self, source, destination):
        if self.game.move(source, destination):
            print('='*30)
            print(f'{self.game.p1_name} move: {source} -> {destination}')
            if self.game.is_game_over():
                self.game_over()
                return True
            if self.AI:
                if (ai_move := self.AI.get_move(self.game.board)):
                    self.game.move(ai_move[0], ai_move[1])
                    print(f'{self.game.p2_name} move: {ai_move[0]} -> {ai_move[1]}')
                    if self.game.is_game_over():
                        self.game_over()
                        return True
                else:
                    self.game_over()
            print(self)
            return True
        else:
            print('Invalid move.\nPlease enter a valid move.\n')
            return False

    def get_scoreboard(self):
        return True

    def get_score(self, player1, player2=None):
        return True

    def play_again(self, yes=True):
        return True
