from abc import ABCMeta
from abc import abstractmethod


class Square:
    def __init__(self, location):
        self.location = location
        self.is_white = None

    def __str__(self):
        return '.'

    def __hash__(self):
        return hash(str(self) + str(self.ID))


class Piece(Square, metaclass=ABCMeta):
    def __init__(self, is_white, location):
        super().__init__(location)
        self.is_white = is_white

    def move(self, location):
        self.location = location

    @abstractmethod
    def moves(self):
        raise NotImplemented


