'''
Integration tests for backend

Format:
name = str
moves = list(move)
  move = 'Origin Destination'
    Origin = '{A,B,C,D,E,F,G,H} {1,2,3,4,5,6,7,8}'
    Destination = '{A,B,C,D,E,F,G,H} {1,2,3,4,5,6,7,8}'
result = list(Pieces)
  - where you expect them to be after moves executed

IE.
name = 'bishop upper right diagonal white movement'
moves = ['D2 D4', 'D7 D5', 'C1 E3', 'C8 E6']
result = [Bishop(is_white=True, location=(4,2)),
          Bishop(is_white=False, location=(4, 5))]
'''

from src.backend.board import Board
from src.backend.pieces.piece import Piece


class IntegrationTest:
    def execute(self, name, moves, result):
        board = Board()
        white_turn = True
        for move in moves:
            # Parse the move
            origin = move.split(' ')[0]
            origin_x, origin_y = ord(origin[0]) - 65, int(origin[1]) - 1
            destination = move.split(' ')[1]
            destination_x, destination_y= ord(destination[0]) - 65, int(destination[1]) - 1
            # Execute the move
            piece = board.board[origin_x][origin_y]
            if ((white_turn and piece.is_white) or (not(white_turn) and not(piece.is_white))) \
                    and board.is_valid_move(piece, (destination_x, destination_y)):
                board.move(piece, (destination_x, destination_y))
                white_turn = not(white_turn)

        # Test for valid state or status
        for piece in result:
            assert isinstance(board[piece.location], piece.__class__), f'{name} failed'
