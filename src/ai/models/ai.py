'''
Abstract Base Class for AI Engines
'''

import abc

class AI(metaclass=ABCMeta):
    def __init__(self, board):
        self.board = board

    @classmethod
    def board_to_datapoint(self):
        return board

    def make_move(self):
        raise NotImplemented

    def get_move(self, move):
        raise NotImplemented
