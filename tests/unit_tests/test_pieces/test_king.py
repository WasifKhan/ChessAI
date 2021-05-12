'''
Unit test for King
'''
from pytest import fixture
from src.backend.pieces.king import King
from src.backend.board import Board


class TestKing:
    @fixture
    def white_king(self):
        return King(is_white=True, location=(4,0))
    
    @fixture
    def black_king(self):
        return King(is_white=False, location=(4,7))

    def test_init(self, white_king, black_king):
        assert white_king.is_white == True
        assert white_king.location[0] == 4
        assert white_king.location[1] == 0
        assert black_king.is_white == False
        assert black_king.location[0] == 4
        assert black_king.location[1] == 7

    def test_str(self, white_king, black_king):
        assert str(white_king) == 'K'
        assert str(black_king) == 'k'

    def test_is_valid_move(self, white_king, black_king):
        board = Board()
        assert white_king.is_valid_move(board, (4,1)) == False
        assert black_king.is_valid_move(board, (4,6)) == False
        board[2,3] = black_king
        black_king.location=(2,3)
        assert black_king.is_valid_move(board, (2,2)) == False
        assert black_king.is_valid_move(board, (3,2)) == False
        assert black_king.is_valid_move(board, (1,2)) == False
        assert black_king.is_valid_move(board, (3,3)) == True
        assert black_king.is_valid_move(board, (1,3)) == True
        assert black_king.is_valid_move(board, (3,4)) == True
        assert black_king.is_valid_move(board, (2,4)) == True
        assert black_king.is_valid_move(board, (1,4)) == True
        board[5,4] = white_king
        white_king.location=(5,4)
        assert white_king.is_valid_move(board, (5,5)) == False
        assert white_king.is_valid_move(board, (4,5)) == False
        assert white_king.is_valid_move(board, (6,5)) == False
        assert white_king.is_valid_move(board, (6,4)) == True
        assert white_king.is_valid_move(board, (4,4)) == True
        assert white_king.is_valid_move(board, (5,3)) == True
        assert white_king.is_valid_move(board, (6,3)) == True
        assert white_king.is_valid_move(board, (4,3)) == True


    def test_moves(self, white_king, black_king):
        board = Board()
        board[5,4] = white_king
        white_king.location=(5,4)
        assert white_king.moves(board) == {44, 43, 53, 63, 64}
        board[2,3] = black_king
        black_king.location=(2,3)
        assert black_king.moves(board) == {13, 14, 24, 34, 33}
        
        


