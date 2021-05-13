'''
Abstract Base Class for AI Engines
'''

from abc import ABCMeta



class AI(metaclass=ABCMeta):
    def __init__(self, location):
        self.location = location

    def train(self, game):
        from ai.data.data_extractor import DataExtractor
        self.data_extractor = DataExtractor(game)
        from os import listdir
        if 'brain.h5' in listdir(self.location):
            from tensorflow.keras.models import load_model
            self.model = load_model(self.location + '/brain.h5')
            return
        self._build_model()
        self._train_model(self.data_extractor.datapoints())
        self._evalulate_model()

    def predict(self, board, is_white):
        prediction = self.model.predict(self.data_extractor.move_to_dp(board, is_white))
        return self.data_extractor.prediction_to_move(prediction)
