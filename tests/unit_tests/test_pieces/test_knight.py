'''
Unit test for Knight
'''
from pytest import fixture
from src.backend.pieces.knight import Knight
from src.backend.board import Board

class TestKnight:
    @fixture
    def white_knight(self):
        return Knight(is_white=True, location=(1,0))

    @fixture
    def black_knight(self):
        return Knight(is_white=False, location=(1,7))

    def test_init(self, white_knight, black_knight):
        assert white_knight.is_white == True
        assert white_knight.location[0] == 1
        assert white_knight.location[1] == 0
        assert black_knight.is_white == False
        assert black_knight.location[0] == 1
        assert black_knight.location[1] == 7

    def test_str(self, white_knight, black_knight):
        assert str(white_knight) == 'N'
        assert str(black_knight) == 'n'

    def test_is_valid_move(self, white_knight, black_knight):
        board = Board()
        assert white_knight.is_valid_move(board, (2,2)) == True
        assert white_knight.is_valid_move(board, (0,2)) == True
        assert white_knight.is_valid_move(board, (3,1)) == False
        assert black_knight.is_valid_move(board, (0,5)) == True
        assert black_knight.is_valid_move(board, (2,5)) == True
        assert black_knight.is_valid_move(board, (3,6)) == False
        board[5,5] = white_knight
        white_knight.location=(5,5)
        assert white_knight.is_valid_move(board, (7,6)) == True
        assert white_knight.is_valid_move(board, (6,7)) == True
        assert white_knight.is_valid_move(board, (4,7)) == True
        assert white_knight.is_valid_move(board, (3,6)) == True
        assert white_knight.is_valid_move(board, (7,4)) == True
        assert white_knight.is_valid_move(board, (6,3)) == True
        assert white_knight.is_valid_move(board, (7,5)) == False
        assert white_knight.is_valid_move(board, (5,7)) == False
        assert white_knight.is_valid_move(board, (7,7)) == False
        assert white_knight.is_valid_move(board, (5,3)) == False

    def test_moves(self, white_knight, black_knight):
        board = Board()
        board[3,4] = white_knight
        white_knight.location =(3,4)
        assert white_knight.moves(board) == {22, 42, 53, 55, 46, 26, 15, 13}
        board[3,3] = black_knight
        black_knight.location =(3,3)
        assert black_knight.moves(board) == {21, 41, 52, 54, 45, 25, 14, 12}

