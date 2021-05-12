'''
Abstract Base Class for AI Engines
'''

from abc import ABCMeta
from os import listdir


class AI(metaclass=ABCMeta):
    def __init__(self, location):
        self.location = location

    def train(self, game):
        if not 'brains.h5' in listdir(self.location):
            self._build_model()
            self._train_model(game)
            self._evaluate_model()
        self.model = load_model(self.location + '/brains.h5')

    def predict(self, board, is_white):
        prediction = self.model.predict(self._board_to_dp(board, is_white))
        return self._prediction_to_board(prediction)
