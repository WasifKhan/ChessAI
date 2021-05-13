'''
Main AI Engine
'''

from .names import MODELS
from abc import ABCMeta


class AI:
    def __init__(self, difficulty=0, name='AI'):
        ai_file, ai_cls = MODELS[difficulty]
        location = f'./ai/models/{ai_file}'
        exec(f'from .models.{ai_file}.{ai_file} import {ai_cls} as ai')
        model = eval('ai')
        self.name = name
        self.model = model(location)

    def train(self, game):
        return self.model.train(game)

    def predict(self, board, is_white=False):
        return self.model.predict(board, is_white)
