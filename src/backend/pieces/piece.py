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

    def __deepcopy__(self, memo):
        return self.__class__(self.is_white, self.location)

    '''
    Delete this function when debugging is done
    '''
    def move(self, location):
        return

    def __str__(self):
        return '.'

    def __hash__(self):
        return hash(str(self) + str(self.ID))

class Piece(Square, metaclass=ABCMeta):
    def __init__(self, is_white, location):
        super().__init__(location)
        self.is_white = is_white
        self.move_IDs = dict()
        self._initialize_moves()

    def move(self, destination):
        for key in self.move_IDs:
            if self.move_IDs[key](self.location) == \
                    destination[0]*10 + destination[1]:
                self.move_ID = key
                break
        self.location = destination
        return
        if self.move_ID == None:
            raise ValueError(f'{str(self)}{str(self.ID)} was not recently moved')

    def get_move(self, move_ID=None):
        if not move_ID:
            return str(self) + str(self.ID) + str(self.move_ID)
        for key in self.move_IDs:
            if key == move_ID:
                return (self.location[0]*10 + self.location[1],
                        self.move_IDs[key](self.location))
        raise IndexError(f'{str(self)}{str(self.ID)} was not recently moved')

    @abstractmethod
    def moves(self, board):
        raise NotImplementedError
