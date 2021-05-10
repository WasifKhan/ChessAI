'''
AI Implemented Using A Convolutional Neural Network
'''

from os import listdir
from ai.models.base_ai import AI
from tensorflow import keras


class ConvNNet(AI):
    def __init__(self, location):
        super().__init__(location)

    def _build_model(self):
        pass

    def _train_model(self):
        pass

    def _evaluate_model(self):
        pass

    def _load_model(self):
        model = keras.models.load_model(self.location + '/weights.h5')
        return model

