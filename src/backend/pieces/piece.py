from abc import ABCMeta
from abc import abstractmethod


class Square:
    ID = 1
    def __init__(self, location):
        self.location = location
        self.ID = Square.ID
        self.is_white = None
        self.value = 0
        Square.ID += 1

    def __str__(self):
        return '.'

    def __hash__(self):
        return hash(str(self) + str(self.ID))

class Piece(Square, metaclass=ABCMeta):
    def __init__(self, is_white, location):
        super().__init__(location)
        self.is_white = is_white
        self.move_IDs = dict()

    def move(self, location):
        self.location = location
        for key in self.move_IDs:
            if self.move_IDs[key](self.location) == location
                self.move_ID = key
                return
        raise ValueError(f'{str(self)}{str(self.ID)} was not recently moved')

    def get_move(self, move_ID=None):
        if not move_ID:
            return self.move_ID
        for key in self.move_IDs:
            if key == move_ID:
                return (self.location[0]*10 + self.location[1],
                        self.move_IDs[key](self.location))
        raise ValueError(f'{str(self)}{str(self.ID)} was not recently moved')

    @abstractmethod
    def moves(self, board):
        raise NotImplementedError
