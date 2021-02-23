import pytest
from src.backend.board import Board
from .tests import moves

def execute(board, name, moves, result):
    white_turn = True
    for move in moves:
        # Parse the move
        origin = move.split(' ')[0]
        origin_x, origin_y = ord(origin[0]) - 65, int(origin[1]) - 1
        destination = move.split(' ')[1]
        destination_x, destination_y= ord(destination[0]) - 65, int(destination[1]) - 1
        invalid_move = False
        # Execute the move
        piece = board.board[origin_x][origin_y]
        if ((white_turn and piece.is_white) or (not(white_turn) and not(piece.is_white))) and piece.is_valid_move(board, (destination_x, destination_y)):
            board.move(piece, (destination_x, destination_y))
            white_turn = not(white_turn)
        else:
            invalid_move = True
    
    # Test for valid state or status
    if 'status' in result:
        assert invalid_move == result['status']
    elif 'state' in result:
        for piece in result['state']:
            assert isinstance(board[piece.location], type(piece))

@pytest.fixture(params=[moves.keys()])
def state(request):
    return Board('testWhite', 'testBlack'), request.param

def test_backend(state):
    board = state[0]
    moves = state[1]
    for move in moves:
        execute(board, move, *(moves[move]))
