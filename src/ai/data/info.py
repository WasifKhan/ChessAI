'''
Metaclass containing AI info
'''


from abc import ABCMeta
from ai.data.logger import Logger



class Info(metaclass=ABCMeta):
    def __init__(self, game, location):
        self.game = game
        self.location = location
        self.logger = Logger().logger
