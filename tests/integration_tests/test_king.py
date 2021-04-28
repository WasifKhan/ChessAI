'''
King Integration Test
'''

from pytest import fixture
from .integration import IntegrationTest
from .pieces.king import moves


class TestKing(IntegrationTest):
    @fixture(params=moves)
    def state(self, request):
        return request.param


    def test_moves(self, state):
        self.execute(*state)

