'''
datapoint:
Size-2 Tuple: (x, y)
X = numpy.array(8,8,1)
Y = numpy.array(142,1)

Board methods:
    print(Board)
    Board[location]: Piece
    Board.move(source, destination)
Piece methods:
    Piece.is_white
    Piece.is_valid_move(board, destination)
    Piece.move(destination)
'''

from ai.models.base_model import BaseModel


class LabeebAI(BaseModel):
    def __init__(self, game, location):
        super().__init__(game, location)

    def train(self):
        '''
        To access datapoints:
        for datapoint in self.datapoints(self.location):
            # Use datapoint...
        '''
        return NotImplemented

    def predict(self, board, is_white):
        return NotImplemented


