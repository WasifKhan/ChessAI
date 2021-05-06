'''
Abstract Base Class for AI Engines
'''

import abc



class AI(metaclass=abc.ABCMeta):
    def __init__(self, is_white=False):
        self.is_white = is_white

    def _board_to_datapoint(self, board):
        datapoint = [[board[column,row].value for column in range(8)] for row in range(8)]
        return datapoint

    def _trained(self):
        raise NotImplemented

    def _train(self):
        raise NotImplemented

    def _predict_move(self, board):
        raise NotImplemented

    def get_move(self, board):
        if not self._trained():
            self._train()
        return self._predict_move(board)
