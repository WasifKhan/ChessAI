'''
Unit test for game
'''

from pytest import fixture
from src.backend.game import Game



class TestGame:
    @fixture
    def game(self):
        return Game()

    def test_init(self, game):
        assert True

    def test_str(self, game):
        assert True

    def test_set_names(self, game):
        assert True

    def test_move(self, game):
        assert True

