'''
AI Implemented Using Deep-Q Networks
'''

from ai.models.base_ai import AI



class DeepQNet(AI):
    def __init__(self, is_white=False):
        self.is_white = is_white

    def _trained(self):
        return True

    def _predict_move(self, board):
        print('got here')
