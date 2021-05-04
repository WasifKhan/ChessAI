'''
Unit test for Bishop
'''
from pytest import fixture
from src.backend.pieces.bishop import Bishop
from src.backend.board import Board

class TestBishop:
    @fixture
    def wite_bishop(self):
        return Bishop(is_white=True, location=(0,2))
    
    @fixture
    def black_bishop(self):
        return Bishop(is_white=False, location=(7,2))

    def test_init(self, black_bishop, white_bishop):
        return True

    def test_str(self):
        return True

    def test_is_valid_move(self):
        return True

    def test_moves(self):
        return True

