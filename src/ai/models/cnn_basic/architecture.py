'''
Data structure storing architecture of CnnBasic network
'''

from copy import copy



class Architecture:
    def __init__(self, name, location):
        performances = {
                'early_game': {'S':list(), 'K':list(), 'Q':list(), 'R':list(),
                    'N':list(), 'B':list(), 'P':list()},
                'mid_game': {'S':list(), 'K':list(), 'Q':list(), 'R':list(),
                    'N':list(), 'B':list(), 'P':list()},
                'late_game': {'S':list(), 'K':list(), 'Q':list(), 'R':list(),
                    'N':list(), 'B':list(), 'P':list()},
                }
        networks = {
                'S': copy([None, list(), list()]),
                'K': copy([None, list(), list()]),
                'Q': copy([None, list(), list()]),
                'R': copy([None, list(), list()]),
                'N': copy([None, list(), list()]),
                'B': copy([None, list(), list()]),
                'P': copy([None, list(), list()]),
            }
        models = {
                'early_game': copy(networks),
                'mid_game': copy(networks),
                'late_game': copy(networks),
            }
        self.models = models
        self.performances = performances
        self.name = name
        self.location = location
        self.load_model()

    def built(self):
        return bool(self.models['early_game']['K'][0])

    def clear_data(self):
        for phase in self.models:
            for network in self.models[phase]:
                self.models[phase][network][1] = list()
                self.models[phase][network][2] = list()

    def add_data(self, phase, network, x_data, y_data):
        self.models[phase][network][1].append(x_data)
        self.models[phase][network][2].append(y_data)

    def prepare_model(self):
        from numpy import array
        for phase in self.models:
            for network in self.models[phase]:
                self.models[phase][network][1] = \
                        array(self.models[phase][network][1])
                self.models[phase][network][2] = \
                        array(self.models[phase][network][2])

    def add_model(self, network, model, phase=None):
        if phase:
            self.models[phase][network][0] = model
        else:
            for phase in self.models:
                self.models[phase][network][0] = model

    def get_model(self, phase, network):
        return self.models[phase][network][0]

    def get_models(self):
        for phase in self.models:
            for network in self.models[phase]:
                yield self.models[phase][network] + [phase, network]
        return StopIteration

    def add_performance(self, performance, phase, network):
        self.performances[phase][network].append(performance)

    def load_model(self):
        from os import listdir
        from keras.models import load_model
        brain_location = self.location + '/brain/'
        for brain in listdir(brain_location):
            if self.name in brain:
                _, p1, p2, network, _ = brain.split('_')
                phase = f'{p1}_{p2}'
                self.models[phase][network][0]=load_model(brain_location + brain)

    def save_model(self):
        for phase in self.models:
            for network in self.models[phase]:
                ID = f'{self.name}_{phase}_{network}_network.h5'
                model = self.models[phase][network][0]
                model.save(f'{self.location}/brain/{ID}')

