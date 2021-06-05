'''
Base Class for AI Engines
'''

from ai.data.data_extractor import DataExtractor



class BaseModel(DataExtractor):
    def __init__(self, game, location):
        super().__init__(game, location)


    def train(self):
        self._build_model()
        self._train_model()
        self._evaluate_model()


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
