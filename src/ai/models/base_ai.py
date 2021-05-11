'''
Abstract Base Class for AI Engines
'''

from abc import ABCMeta
from os import listdir


class AI(metaclass=ABCMeta):
    def __init__(self, location):
        self.location = location
        if not self._trained():
            self._build_model()
            self._train_model()
            self._evaluate_model()

    def _trained(self):
        return True if 'brain.h5' in listdir(self.location) else False

    def _get_datapoint(self):
        dataset_path = './ai/data/dataset/'
        for data in listdir(dataset_path):
            if data[0] == 'd':
                with open(dataset_path + data) as fp:
                    for moves in fp:
                        yield self._generate_datapoint(moves)

    def _resign(self, board, is_white):
        if len(board.history) < 3:
            return False
        prior_turns = [board.history[i][3] for i in range(-3, 0, 1)]
        if is_white and max(prior_turns) <= -2 \
            or (not is_white and min(prior_turns) >= 2):
                return True
        return False

    def _predict_move(self, board, is_white):
        if not self.model:
            self._load_model()
        prediction = self.model.predict(self._board_to_datapoint(board, is_white))
        return self._prediction_to_board(prediction)

    def get_move(self, board, is_white):
        return False if self._resign(board, is_white) else self._predict_move(board, is_white)
