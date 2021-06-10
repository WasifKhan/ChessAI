'''
Data structure storing architecture of CnnBasic network
'''



class Architecture:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.performances = {'S':list(), 'K':list(), 'Q':list(), 'R':list(),
                'N':list(), 'B':list(), 'P':list()}
        self.models = {
                'S': [None, list(), list()],
                'K': [None, list(), list()],
                'Q': [None, list(), list()],
                'R': [None, list(), list()],
                'N': [None, list(), list()],
                'B': [None, list(), list()],
                'P': [None, list(), list()],
            }
        self.load_model()


    def built(self):
        return bool(self.models['S'][0])


    def clear_data(self):
        for network in self.models:
            self.models[network][1] = list()
            self.models[network][2] = list()

    def add_data(self, network, x_data, y_data):
        self.models[network][1].append(x_data)
        self.models[network][2].append(y_data)

    def prepare_model(self):
        from numpy import array
        for network in self.models:
            self.models[network][1] = \
                    array(self.models[network][1])
            self.models[network][2] = \
                    array(self.models[network][2])

    def add_model(self, piece, model):
        self.models[str(piece)][0] = model

    def get_model(self, network):
        return self.models[network][0]

    def get_models(self):
        for network in self.models:
            yield self.models[network] + [network]
        return StopIteration

    def add_performance(self, performance, network):
        self.performances[network].append(performance)

    def load_model(self):
        from os import listdir
        from tensorflow.keras.models import load_model
        brain_location = self.location + '/brain/'
        for brain in listdir(brain_location):
            if self.name in brain:
                _, p1, _ = brain.split('_')
                self.models[network][0]=load_model(brain_location + brain)

    def save_model(self):
        for network in self.models[phase]:
            ID = f'{self.name}_{network}_network.h5'
            model = self.models[network][0]
            model.save(f'{self.location}/brain/{ID}')

