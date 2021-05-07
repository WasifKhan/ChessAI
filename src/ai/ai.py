'''
Main AI Engine
'''

from .names import MODELS



class AI:
    def __init__(self, name='AI', difficulty=0):
        self.name = name
        ai_file, ai_cls = MODELS[difficulty]
        exec(f'from .models.{ai_file}.{ai_file} import {ai_cls} as ai')
        model = eval('ai')
        self.ai = model()

    def get_move(self, board):
        return self.ai.get_move(board)
