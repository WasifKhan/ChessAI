'''
Base Class for AI Engines
'''

from abc import ABCMeta


class BaseModel(metaclass=ABCMeta):
    def __init__(self, game, location, logger):
        self.game = game
        self.location = location
        self.logger = logger

    def train(self):
        self.download_raw_data()
        #self.clean_memory()
        #self.clean_data()
        #self._train_model()
        #self._evaluate_model()

    def _resign(self, board, is_white):
        if len(board.history) >= 5:
            value = sum([value[3] for value in board.history[-5:]])
            if (value <= -15 and is_white) or (value >= 15 and not is_white):
                return True
        return False

    def predict(self, board, is_white):
        if self._resign(board, is_white):
            return False
        return self._predict(board, is_white)
