'''
Main AI Engine
'''

from .names import MODELS
from .data.data_extrator import data_extractor



class AI:
    def __init__(self, difficulty=0, name='AI'):
        # The following line take approximately 15 hours to run to train AI
        data_extractor.raw_data_to_dataset()

        ai_file, ai_cls = MODELS[difficulty]
        location = f'./ai/models/{ai_file}'
        exec(f'from .models.{ai_file}.{ai_file} import {ai_cls} as ai')
        model = eval('ai')
        self.name = name
        self.ai = model(location)

    def get_move(self, board, is_white=False):
        return self.ai.get_move(board, is_white)
