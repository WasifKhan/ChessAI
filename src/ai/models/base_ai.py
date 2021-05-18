'''
Abstract Base Class for AI Engines
'''

from abc import ABCMeta



class AI(metaclass=ABCMeta):
    def __init__(self, location):
        self.location = location
        from os import listdir
        if 'brain.h5' in listdir(self.location):
            from tensorflow.keras.models import load_model
            self.model = load_model(self.location + '/brain.h5')

    def train(self, game):
        from ai.data.data_extractor import DataExtractor
        self.data_extractor = DataExtractor(game)
        from os import listdir
        if 'brain.h5' in listdir(self.location):
            from tensorflow.keras.models import load_model
            self.model = load_model(self.location + '/brain.h5')
        else:
            self._build_model()
        self._train_model(self.data_extractor.datapoints(self.location))
        self._evaluate_model()

    def _resign(self, board, is_white):
        if len(board.history) >= 5:
            value = sum([value[3] for value in board.history[-5:]])
            if (value <= -10 and is_white) or (value >= 10 and not is_white):
                return True
        return False

    def predict(self, board, is_white):
        if self._resign(board, is_white):
            return False
        prediction = self.model.predict(self.data_extractor._board_to_datapoint(board, is_white))
        move = self.data_extractor._prediction_to_move(prediction, board, is_white)
        return move

