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

    def _should_resign(self, board):
        if len(board.history) < 4:
            return False
        turns_ago_2 = board.history[-3][3]
        turn_ago_1 = board.history[-1][3]
        if self.is_white:
            if turns_ago_2 <= -2 and turn_ago_1 <= -2:
                return True
            else:
                return False
        else:
            if turns_ago_2 >= 2 and turn_ago_1 >= 2:
                return True
            else:
                return False

    def _predict_move(self, board):
        raise NotImplemented

    def get_move(self, board):
        if not self._trained():
            self._train()
        return None if self._should_resign(board) else self._predict_move(board)
