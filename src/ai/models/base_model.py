'''
Abstract Base Class for AI Engines
'''

from abc import ABCMeta



DOWNLOAD_DATA = True


class BaseModel(metaclass=ABCMeta):
    def __init__(self, game, location):
        from os import listdir
        from ai.data.data_extractor import DataExtractor
        self.location = location
        self.datapoints = DataExtractor(game, location, DOWNLOAD_DATA).datapoints
        self.game = game
        if hasattr(self, '_load_model'):
            self._load_model()

    def train(self):
        if hasattr(self, '_train'):
            self._train()

    def _resign(self, board, is_white):
        if len(board.history) >= 5:
            value = sum([value[3] for value in board.history[-5:]])
            if (value <= -10 and is_white) or (value >= 10 and not is_white):
                return True
        return False

    def predict(self, board, is_white):
        if self._resign(board, is_white):
            return False
        return self._predict(board, is_white)
