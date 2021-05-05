'''
Abstract Base Class for AI Engines
'''

import abc



class AI(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @classmethod
    def board_to_datapoint(self):
        return self.board

    def make_move(self):
        raise NotImplemented

    def get_move(self, move):
        raise NotImplemented
