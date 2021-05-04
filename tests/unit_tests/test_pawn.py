'''
Unit test for Pawn
'''

from pytest import fixture
from src.backend.pieces.pawn import Pawn
from src.backend.board import Board



class TestPawn:
    @fixture
    def white_pawn(self):
        return Pawn(is_white=True, location=(1, 0))


    @fixture
    def black_pawn(self):
        return Pawn(is_white=False, location=(6, 6))


    def test_init(self, white_pawn, black_pawn):
        assert white_pawn.is_white == True
        assert white_pawn.location[0] == 1
        assert white_pawn.location[1] == 0
        assert black_pawn.is_white == False
        assert black_pawn.location[0] == 6
        assert black_pawn.location[1] == 6


    def test_str(self, white_pawn, black_pawn):
        assert str(white_pawn) == 'P'
        assert str(black_pawn) == 'p'


    def test_is_valid_move(self, white_pawn, black_pawn):
        board = Board()
        assert white_pawn.is_valid_move(board, (2,0)) == True
        assert white_pawn.is_valid_move(board, (3,0)) == True
        assert white_pawn.is_valid_move(board, (0,4)) == False
        assert white_pawn.is_valid_move(board, (4,0)) == False
        assert black_pawn.is_valid_move(board, (5,6)) == True
        assert black_pawn.is_valid_move(board, (4,6)) == True
        assert black_pawn.is_valid_move(board, (6,3)) == False
        assert black_pawn.is_valid_move(board, (7,6)) == False
        board[4,4] = white_pawn
        white_pawn.location=(4,4)
        assert white_pawn.is_valid_move(board, (5,4)) == True
        assert white_pawn.is_valid_move(board, (6,4)) == False
        assert white_pawn.is_valid_move(board, (4,5)) == False
        board[5,5] = black_pawn
        black_pawn.location=(5,5)
        assert black_pawn.is_valid_move(board, (4,5)) == True
        assert black_pawn.is_valid_move(board, (4,4)) == True
        assert black_pawn.is_valid_move(board, (4,6)) == False


    def test_moves(self, white_pawn, black_pawn):
        board = Board()
        print(white_pawn.moves(board))
        print(black_pawn.moves(board))
        assert white_pawn.moves(board) == {2, 3}
        assert black_pawn.moves(board) == {56, 46}
        board[5,5] = white_pawn
        white_pawn.location=(5,5)
        assert white_pawn.moves(board) == {64, 66}
