'''
Abstract Base Class for AI Engines
'''

import abc



class AI(metaclass=abc.ABCMeta):
    def __init__(self, is_white=False):
        self.is_white = is_white

    def _train(self):
        raise NotImplemented

    def _load_weights(self):
        raise NotImplemented

    @classmethod
    def board_to_datapoint(self):
        return self.board

    def make_move(self):
        raise NotImplemented

    def get_move(self, move):
        raise NotImplemented
