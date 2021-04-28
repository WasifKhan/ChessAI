'''
Knight Integration Test
'''

from pytest import fixture
from .integration import IntegrationTest
from .pieces.knight import moves


class TestKnight(IntegrationTest):
    @fixture(params=moves)
    def state(self, request):
        return request.param

    def test_moves(self, state):
        self.execute(*state)

