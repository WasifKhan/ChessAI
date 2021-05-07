'''
Unit test for Rook
'''
from pytest import fixture
from src.backend.pieces.rook import Rook
from src.backend.board import Board

class TestRook:
    @fixture
    def white_rook(self):
        return Rook(is_white=True, location=(0,0))
    
    @fixture
    def black_rook(self):
        return Rook(is_white=False, location=(0,7))

    def test_init(self, white_rook, black_rook):
        assert white_rook.is_white == True
        assert white_rook.location[0] == 0
        assert white_rook.location[1] == 0
        assert black_rook.is_white == False
        assert black_rook.location[0] == 0
        assert black_rook.location[1] == 7

    def test_str(self, white_rook, black_rook):
        assert str(white_rook) == 'R'
        assert str(black_rook) == 'r'

    def test_is_valid_move(self, white_rook, black_rook):
        board = Board()
        assert white_rook.is_valid_move(board, (1,1)) == False
        assert black_rook.is_valid_move(board, (1,6)) == False
        board[2,3] = white_rook
        white_rook.location=(2,3)
        assert white_rook.is_valid_move(board, (2,2)) == True
        assert white_rook.is_valid_move(board, (0,3)) == True
        assert white_rook.is_valid_move(board, (2,6)) == True
        assert white_rook.is_valid_move(board, (7,3)) == True
        assert white_rook.is_valid_move(board, (4,6)) == False
        assert white_rook.is_valid_move(board, (7,6)) == False
        board[3,3] = black_rook
        black_rook.location=(3,3)
        assert black_rook.is_valid_move(board, (2,3)) == True
        assert black_rook.is_valid_move(board, (7,3)) == True
        assert black_rook.is_valid_move(board, (3,5)) == True
        assert black_rook.is_valid_move(board, (3,1)) == True
        assert black_rook.is_valid_move(board, (4,2)) == False
        assert black_rook.is_valid_move(board, (5,5)) == False
        assert black_rook.is_valid_move(board, (3,6)) == False
        assert black_rook.is_valid_move(board, (0,3)) == False


    def test_moves(self, white_rook, black_rook):
        board = Board()
        board[2,3] = white_rook
        white_rook.location=(2,3)
        board[3,3] = black_rook
        black_rook.location=(3,3)
        assert white_rook.moves(board) == {22, 13, 3, 24, 25, 26, 33}
        assert black_rook.moves(board) == {23, 32, 31, 43,53, 63, 73, 34, 35}

