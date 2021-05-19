'''
Unit test for Bishop
'''
from pytest import fixture
from src.backend.pieces.bishop import Bishop
from src.backend.board import Board

class TestBishop:
    @fixture
    def white_bishop(self):
        return Bishop(is_white=True, location=(5,0))
    
    @fixture
    def black_bishop(self):
        return Bishop(is_white=False, location=(2,7))

    def test_init(self, white_bishop, black_bishop):
        assert white_bishop.is_white == True
        assert white_bishop.location[0] == 5
        assert white_bishop.location[1] == 0
        assert black_bishop.is_white == False
        assert black_bishop.location[0] == 2
        assert black_bishop.location[1] == 7

    def test_str(self, white_bishop, black_bishop):
        assert str(white_bishop) == 'B'
        assert str(black_bishop) == 'b'

    def test_is_valid_move(self, white_bishop, black_bishop):
        board = Board()
        assert white_bishop.is_valid_move(board, (1,3)) == False
        assert white_bishop.is_valid_move(board, (1,1)) == False
        assert black_bishop.is_valid_move(board, (1,6)) == False
        assert black_bishop.is_valid_move(board, (3,6)) == False
        board[3,4] = white_bishop
        white_bishop.location=(3,4)
        assert white_bishop.is_valid_move(board, (2,3)) == True
        assert white_bishop.is_valid_move(board, (1,2)) == True
        assert white_bishop.is_valid_move(board, (5,6)) == True
        assert white_bishop.is_valid_move(board, (1,6)) == True
        assert white_bishop.is_valid_move(board, (5,2)) == True
        assert white_bishop.is_valid_move(board, (3,3)) == False
        assert white_bishop.is_valid_move(board, (3,5)) == False
        assert white_bishop.is_valid_move(board, (2,4)) == False
        board[4,3] = black_bishop
        black_bishop.location=(4,3)
        assert black_bishop.is_valid_move(board, (2,1)) == True
        assert black_bishop.is_valid_move(board, (6,1)) == True
        assert black_bishop.is_valid_move(board, (6,5)) == True
        assert black_bishop.is_valid_move(board, (2,5)) == False
        assert black_bishop.is_valid_move(board, (4,2)) == False
        assert black_bishop.is_valid_move(board, (7,6)) == False
        assert black_bishop.is_valid_move(board, (3,5)) == False


    def test_moves(self, white_bishop, black_bishop):
        board = Board()
        board[3,2] = white_bishop
        white_bishop.location=(3,2)
        assert white_bishop.moves(board) == {5, 14, 23, 43, 54, 65, 76}
        board[4,5] = black_bishop
        black_bishop.location=(4,5)
        assert black_bishop.moves(board) == {34, 23, 12, 1, 54, 63, 72}

