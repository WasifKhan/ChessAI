'''
Interface between backend and frontend
'''


from backend.game import Game
from ai.ai import AI



class Interface:
    def __init__(self):
        self.game = Game()
        self.versus_ai = False

    def __str__(self):
        return str(self.game)

    def versus_AI(self, difficulty) -> None:
        self.ai = AI(self.game, difficulty)
        self.versus_ai = True
        self.set_player_names(self.game.p1_name, self.ai.name)

    def train_AI(self):
        self.ai.train()

    def set_player_names(self, p1_name: str, p2_name: str) -> None:
        self.game.set_names(p1_name, p2_name)

    def game_over(self) -> None:
        print('*'*30)
        winner = not(self.game.white_turn)
        if not self.game.is_game_over():
            loser = self.game.p1_name if self.game.white_turn else self.game.p2_name
            print('*' * 7 + f'{loser} resigned' + '*' * 6)
        print(('*'*30 + '\n') + ('*'*11 + 'GAME OVER' + '*'*10 + '\n') + ('*'*30))
        self.game.game_over(1, 0) if winner else self.game.game_over(0, 1)
        self.play_again()

    def ai_move(self, is_white: bool) -> bool:
        return self.add_move(ai_move[0], ai_move[1]) \
                if (ai_move := self.ai.predict(self.game.board, is_white)) \
                else ai_move

    def add_move(self, source: int, destination: int) -> bool:
        if self.game.move(source, destination):
            name = self.game.p2_name if self.game.white_turn else self.game.p1_name
            print(f'{name} move: {source} -> {destination}')
            if self.game.is_game_over():
                self.game_over()
                return True
            return True
        print('Invalid move.\nPlease enter a valid move.\n')
        return False

    def simulate_games(self, num_games: int):
        white_wins, black_wins = 0,0
        for i in range(num_games):
            self.game = Game('Wasif AI', 'Ali AI')
            white_ai = AI(self.game, 0)
            black_ai = AI(self.game, 4)
            AIs = [white_ai, black_ai]
            white_turn = True
            while not self.game.is_game_over():
                move = AIs[int(not white_turn)].predict(self.game.board, white_turn)
                if not move or not self.add_move(*move):
                    break
                white_turn = not(white_turn)
            if not(self.game.white_turn):
                white_wins += 1
                print('White wins')
            else:
                black_wins += 1
                print('Black wins')
        self.game = Game('Player 1', 'Black AI')
        self.game.game_over(white_wins, black_wins)
        print(f'score: {white_wins}-{black_wins}')

    def play_again(self, yes: bool=True):
        print('*'*30 + '\n')
        print('Reseting game...')
        print('*'*30 + '\n')
        self.game = Game(self.game.p1_name, self.game.p2_name)
        print(self)
        return True

    def get_scoreboard(self):
        return self.game.get_scoreboard()

    def get_score(self, player1: str, player2: str=None):
        return self.game.get_score(player1, player2)


