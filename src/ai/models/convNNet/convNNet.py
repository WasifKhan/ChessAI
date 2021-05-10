'''
AI Implemented Using A Convolutional Neural Network
'''

from os import listdir
from ai.models.base_ai import AI



class ConvNNet(AI):
    def __init__(self):
        super().__init__()

    def _trained(self):
        return True if 'weights.txt' in listdir('ai/models/convNNet/') else False

    def _train(self):
        return True

    def _predict_move(self, board):
        print('got here')
