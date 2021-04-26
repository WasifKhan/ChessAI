import pytest
from src.backend.board import Board
from src.backend.piece import Piece
from .tests import moves

def execute(name, moves, result):
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
        if ((white_turn and piece.is_white) or (not(white_turn) and not(piece.is_white))) and piece.is_valid_move(board, (destination_x, destination_y)):
            board.move(piece, (destination_x, destination_y))
            white_turn = not(white_turn)

    # Test for valid state or status
    for piece in result:
        if not(isinstance(piece, Piece)):
            assert not(isinstance(board[piece.location], Piece)), f'{name} failed'
        else:
            assert isinstance(board[piece.location], type(piece)), f'{name} failed'

@pytest.fixture(params=moves)
def state(request):
    return request.param

def test_backend(state):
    execute(*state)

