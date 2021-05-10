'''
Abstract Base Class for AI Engines
'''

from abc import ABCMeta
from os import listdir



class AI(metaclass=ABCMeta):
    def __init__(self):
        if not self._trained():
            self._train()

    def _trained(self):
        raise NotImplemented

    def _train(self):
        raise NotImplemented

    def _predict_move(self, board, is_white):
        raise NotImplemented

    def _board_to_datapoint(self, board):
        datapoint = [[(board[column,row].value, board[column,row].is_white) for column in range(8)] for row in range(8)]
        return datapoint

    def _generate_datapoint(self, moves):
        return moves

    def _get_data_points(self):
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

    def get_move(self, board, is_white):
        return False if self._resign(board, is_white) else self._predict_move(board, is_white)
