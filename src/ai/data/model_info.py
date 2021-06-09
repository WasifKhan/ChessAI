'''
Metaclass containing AI info
'''

from ai.data.logger import Logger
from ai.data.data_extractor import DataExtractor



class ModelInfo(DataExtractor):
    def __init__(self, game, location):
        logger = Logger().logger
        super().__init__(game, location, logger)

