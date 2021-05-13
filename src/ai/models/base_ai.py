'''
Abstract Base Class for AI Engines
'''

from abc import ABCMeta



class AI(metaclass=ABCMeta):
    def __init__(self, location):
        self.location = location

    def train(self, game):
        from os import listdir
        if 'brain.h5' in listdir(self.location):
            self.model = load_model(self.location + '/brains.h5')
            return
        from ai.data.data_extractor import DataExtractor
        datapoints = DataExtractor(game).datapoints()
        self._build_model()
        self._train_model(datapoints)
        self._evalulate_model()

    def predict(self, board, is_white):
        prediction = self.model.predict(self._board_to_dp(board, is_white))
        return self._prediction_to_board(prediction)
