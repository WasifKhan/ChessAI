'''
Unit test for Bishop
'''
from pytest import fixture
from src.backend.pieces.bishop import Bishop
from src.backend.board import Board

class TestBishop:
    @fixture
    def white_bishop(self):
        return Bishop(is_white=True, location=(0,2))
    
    @fixture
    def black_bishop(self):
        return Bishop(is_white=False, location=(7,2))

    def test_init(self, black_bishop, white_bishop):
        assert white_bishop.is_white == True
        assert white_bishop.location[0] == 0
        assert white_bishop.location[1] == 2
        assert black_bishop.is_white == False
        assert black_bishop.location[0] == 7
        assert black_bishop.location[1] == 2

    def test_str(self, white_bishop, black_bishop):
        assert str(white_bishop) == 'B'
        assert str(black_bishop) == 'b'

    def test_is_valid_move(self, black_bishop, white_bishop):
        board = Board()
        assert white_bishop.is_valid_move(board, (1,3)) == False
        assert white_bishop.is_valid_move(board, (1,0)) == False
        board[3,3] = white_bishop
        white_bishop.location=(3,3)
        assert white_bishop.is_valid_move(board, (4,4)) == True
        assert white_bishop.is_valid_move(board, (5,5)) == True
        assert white_bishop.is_valid_move(board, (6,6)) == True
        assert white_bishop.is_valid_move(board, (4,2)) == True
        assert white_bishop.is_valid_move(board, (6,0)) == True
        assert white_bishop.is_valid_move(board, (4,3)) == False
        assert white_bishop.is_valid_move(board, (2,3)) == False
        assert white_bishop.is_valid_move(board, (2,2)) == True
        assert white_bishop.is_valid_move(board, (1,1)) == False
        board[3,4] = black_bishop
        black_bishop.location=(3,4)
        assert black_bishop.is_valid_move(board, (1,3)) == False
        assert black_bishop.is_valid_move(board, (2,3)) == True
        assert black_bishop.is_valid_move(board, (1,2)) == True
        assert black_bishop.is_valid_move(board, (1,6)) == True
        assert black_bishop.is_valid_move(board, (5,6)) == True
        assert black_bishop.is_valid_move(board, (5,2)) == True

        

    def test_moves(self):
        return True

