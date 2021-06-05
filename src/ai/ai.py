'''
Main AI Engine
'''

from .models.names import MODELS



class AI:
    def __init__(self, game, difficulty=0):
        ai_file, ai_cls = MODELS[difficulty]
        location = f'./ai/models/{ai_file}'
        exec(f'from .models.{ai_file}.{ai_file} import {ai_cls} as ai')
        model = eval('ai')
        self.name = ai_cls
        self.ai = model(game, location)
        message = ('*'*20 + '\n')*3 + f'Loaded {ai_cls}\n' + ('*'*20 + '\n')*3
        self.ai.logger.info(message)

    def train(self):
        return self.ai.train()

    def predict(self, board, is_white=False):
        return self.ai.predict(board, is_white)
