class Genetic:
    def __init__(self, players):
        self.players = players

    def play_game(self):
        results = dict()
        for player in players:
            result = player[player].play()
            results[player] = result

        sorted_results sorted(list(results.values()), key= lambda x: -x)
        for player in results:
            if results[player] in set(sorted_results[0:3]):
                new_player = self.players[player].reproduce()
                self.add_player(new_player)
            elif results[player] in set(sorted_results[-3:-1]):
                self.kill_player(self.players[player])






