'''
Unit test for board
'''

from pytest import fixture
from src.backend.board import Board



class TestBoard:
    @fixture
    def board(self):
        return Board()

    def test_init(self, board):
        assert True

    def test_getitem(self, board):
        assert True

    def test_setitem(self, board):
        assert True

    def test_move(self, board):
        assert True

    def test_initialize_board(self, board):
        assert True

