'''
Abstract Base Class for AI Engines
'''

from abc import ABCMeta



class BaseModel(metaclass=ABCMeta):
    def __init__(self, game, location):
        from os import listdir
        from ai.data.data_extractor import DataExtractor
        self.location = location
        self.datapoints = DataExtractor(game, location).datapoints
        self.game = game
        if 'brain.h5' in listdir(self.location):
            from tensorflow.keras.models import load_model
            self.model = load_model(self.location + '/brain.h5')


    def train(self):
        if not hasattr(self, 'model'):
            self._build_model()
        self._train_model()
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
        prediction = self.model.predict(self._board_to_datapoint(board, is_white))
        move = self._prediction_to_move(prediction, board, is_white)
        return move

