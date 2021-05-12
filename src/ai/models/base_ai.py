'''
Abstract Base Class for AI Engines
'''

from abc import ABCMeta



class AI(metaclass=ABCMeta):
    def __init__(self, location):
        self.location = location

    def train(self, game):
        if not self.model:
            self._build_model(game)

    def predict(self, board, is_white):
        prediction = self.model.predict(self._board_to_dp(board, is_white))
        return self._prediction_to_board(prediction)
