from abc import ABCMeta
from abc import abstractmethod


class Square:
    ID = 1
    def __init__(self, location, ID=None):
        self.location = location
        self.ID = ID if ID else Square.ID
        self.is_white = None
        self.value = 0

    def __copy__(self):
        if isinstance(self, Piece):
            return self.__class__(self.ID, self.is_white, self.location)
        return Square(self.location, self.ID)

    def __eq__(self, other):
        return self.value == other.value \
                and self.ID == other.ID \
                and self.location == other.location

    def __str__(self):
        return '.'

    def __hash__(self):
        return hash(str(self) + str(self.ID))

    def compute_info(self, board):
        if not isinstance(self, Piece):
            self.defends, self.threats, self.threatens, self.num_moves = [0]*4
            return
        my_pieces, their_pieces = (board.white_pieces, board.black_pieces) \
                if self.is_white else (board.black_pieces, board.white_pieces)
        self.defends = sum([piece.value for piece in my_pieces \
                if piece.location[0]*10 + piece.location[1] in self.moves(board)])
        self.threats = sum([self.value for piece in their_pieces \
                if self.location[0]*10 + self.location[1] in piece.moves(board)])
        self.threatens = sum([piece.value for piece in their_pieces \
                if piece.location[0]*10 + piece.location[1] in self.moves(board)])
        self.num_moves = sum([1 for move in self.moves(board) \
                if not isinstance(board[move], Piece)])


class Piece(Square, metaclass=ABCMeta):
    def __init__(self, is_white, location):
        super().__init__(location)
        self.is_white = is_white
        self.move_IDs = dict()
        self._initialize_moves()

    def move(self, destination):
        self.move_ID = None
        for key in self.move_IDs:
            if self.move_IDs[key](self.location) == \
                    destination[0]*10 + destination[1]:
                self.move_ID = key
                break
        else:
            raise AttributeError(f'Cannot find move for {str(self)}')
        self.location = destination

    def get_move(self, move_ID):
        for key in self.move_IDs:
            if key == move_ID:
                return (self.location[0]*10 + self.location[1],
                        self.move_IDs[key](self.location))
        raise AttributeError(f'{str(self)}{str(self.ID)} was not recently moved')

    @abstractmethod
    def moves(self, board):
        raise NotImplementedError
