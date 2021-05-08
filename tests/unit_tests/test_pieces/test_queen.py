'''
Unit test for Queen
'''
from pytest import fixture
from src.backend.pieces.queen import Queen
from src.backend.board import Board

class TestQueen:
    @fixture
    def white_queen(self):
        return Queen(is_white=True, location=(3,0))
    
    @fixture
    def black_queen(self):
        return Queen(is_white=False, location=(3,7))

    def test_init(self, white_queen, black_queen):
        assert white_queen.is_white == True
        assert white_queen.location[0] == 3
        assert white_queen.location[1] == 0
        assert black_queen.is_white == False
        assert black_queen.location[0] == 3
        assert black_queen.location[1] == 7

    def test_str(self, white_queen, black_queen):
        assert str(white_queen) == 'Q'
        assert str(black_queen) == 'q'

    def test_is_valid_move(self, white_queen, black_queen):
        board = Board()
        assert white_queen.is_valid_move(board, (3,2)) == False
        assert black_queen.is_valid_move(board, (3,5)) == False
        board[2,3] = white_queen
        white_queen.location=(2,3)
        assert white_queen.is_valid_move(board, (5,6)) == True
        assert white_queen.is_valid_move(board, (2,6)) == True
        assert white_queen.is_valid_move(board, (7,3)) == True
        assert white_queen.is_valid_move(board, (3,2)) == True
        assert white_queen.is_valid_move(board, (0,5)) == True
        assert white_queen.is_valid_move(board, (2,4)) == True
        assert white_queen.is_valid_move(board, (2,1)) == False
        assert white_queen.is_valid_move(board, (4,2)) == False
        assert white_queen.is_valid_move(board, (5,4)) == False
        assert white_queen.is_valid_move(board, (7,5)) == False
        assert white_queen.is_valid_move(board, (0,1)) == False
        board[3,3] = black_queen
        black_queen.location=(3,3)
        assert black_queen.is_valid_move(board, (3,1)) == True
        assert black_queen.is_valid_move(board, (1,1)) == True
        assert black_queen.is_valid_move(board, (5,1)) == True
        assert black_queen.is_valid_move(board, (5,5)) == True
        assert black_queen.is_valid_move(board, (1,5)) == True
        assert black_queen.is_valid_move(board, (3,5)) == True
        assert black_queen.is_valid_move(board, (3,6)) == False
        assert black_queen.is_valid_move(board, (0,6)) == False
        assert black_queen.is_valid_move(board, (5,4)) == False
        assert black_queen.is_valid_move(board, (4,5)) == False
        assert black_queen.is_valid_move(board, (6,6)) == False


        

    def test_moves(self, white_queen, black_queen):
        board = Board()
        board[2,3] = white_queen
        white_queen.location=(2,3)
        assert white_queen.moves(board) == {33 ,43, 53, 63, 73, 32, 22, 12, 13, 3, 14, 5, 24, 25, 26, 34, 45, 56}
        board[4,3] = black_queen
        black_queen.location=(4,3)
        assert black_queen.moves(board) == {33, 23, 32, 21, 42, 41, 52, 61, 53, 63, 73, 54, 65, 44, 45, 34, 25}


