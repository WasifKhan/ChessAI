'''
Main AI Engine
'''

from .models.names import MODELS



class AI:
    def __init__(self, game, difficulty=0, name='AI'):
        ai_file, ai_cls = MODELS[difficulty]
        location = f'./ai/models/{ai_file}'
        exec(f'from .models.{ai_file}.{ai_file} import {ai_cls} as ai')
        model = eval('ai')
        self.name = name
        self.ai = model(game, location)

    def train(self):
        return self.ai.train()

    def predict(self, board, is_white=False):
        return self.ai.predict(board, is_white)
