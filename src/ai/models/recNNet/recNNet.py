'''
AI Implemented Using A Recurrent Neural Network
'''

from ai.models.base_model import BaseModel



class RecNNet(BaseModel):
    def __init__(self, is_white=False):
        self.is_white = is_white

    def _trained(self):
        return True

    def _train(self):
        return True

    def _predict_move(self, board):
        print('got here')
