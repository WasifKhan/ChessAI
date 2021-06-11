'''
Data structure storing architecture of CnnBasic network
'''

from tensorflow.keras.optimizers import SGD, Adam, RMSprop
from tensorflow.keras.initializers import RandomUniform as RU,\
        RandomNormal as RN


class Architecture:
    def __init__(self, location):
        self.location = location
        self.configurations = list()
        self.performances = dict()
        self.models = dict()
        self._load_configurations()
        self._load_model()


    def _load_configurations(self):
        from itertools import product
        layer_infos = [
                (1, [16], [(4, 4)], ['relu']),
                (1, [32], [(4, 4)], ['relu']),
                (2, [16, 32], [(4, 4), (3, 3)], ['relu']*2),
                (2, [32, 64], [(4, 4), (3, 3)], ['relu']*2),
                (3, [16, 32, 64], [(4, 4), (3, 3), (2, 2)], ['relu']*3),
                (3, [32, 64, 128], [(3, 3), (2, 2), (1, 1)], ['relu']*3),
                ]
        initializers = [
                RU(minval=0.0000001, maxval=0.000001),
                RU(minval=0.00001, maxval=0.0001),
                RN(mean=0, stddev=0.0000001),
                RN(mean=0, stddev=0.00001),
                ]
        optimizers =
                RMSprop(),
                SGD(learning_rate=0.001),
                Adam(),
                ]
        loss_metrics = [
                ('categorical_crossentropy', 'loss'),
                ('sigmoid', 'loss'),
                ]
        for info in product(layer_infos, initializers, optimizers, loss_metrics):
            layer_info, initializer, optimizer, loss_metric = info
            num_layers = layer_info[0]
            density = 'Sparse' if layer_info[1][0] == 16 else 'Dense'
            init = 'Uniform' if str(initializer) == str(RU) else 'Normal'
            init_config = 'Small' if (init == 'Uniform' \
                    and initializer.get_config()['minval'] == 0.00001) \
                    or (init == 'Normal' \
                    and initializer.get_config()['stddev'] = 0.00001) \
                    else 'Large'
            optimizer = 'Adam' if str(Adam) == str(optimizer) \
                    else 'SGD' if str(SGD) == str(optimizer) \
                    else 'RMSprop'
            activation = 'Sigmoid' if loss_metric[0] == 'sigmoid' else 'Categorical-Crossentropy'
            ID = f'''
            {num_layers} {denisty} layers. \
            {init_config} {init} weight initialization. \
            {optimizer} optimizer. {activation} activation.\
            '''
            self.models[ID] = {
                'S': [None, list(), list()],
                'K': [None, list(), list()],
                'Q': [None, list(), list()],
                'R': [None, list(), list()],
                'N': [None, list(), list()],
                'B': [None, list(), list()],
                'P': [None, list(), list()],
                }
            self.performances[ID] = {
                    'S':list(), 'K':list(), 'Q':list(), 'R':list(),
                    'N':list(), 'B':list(), 'P':list()
                }
            self.configurations[ID] = info


    def _load_model(self):
        from os import listdir
        from tensorflow.keras.models import load_model
        brain_location = self.location + '/brain/'
        for brain in listdir(brain_location):
            if '.h5' in brain:
                name = brain.split('_')
                ID = name[0:11].join('_')
                network = name[11]
                self.models[ID][network][0] = load_model(brain_location + brain)


    def built(self):
        return bool(self.models)


    def clear_data(self, ID):
        for network in self.models:
            self.models[ID][network][1] = list()
            self.models[ID][network][2] = list()


    def add_data(self, ID, network, x_data, y_data):
        self.models[ID][network][1].append(x_data)
        self.models[ID][network][2].append(y_data)


    def prepare_model(self, ID):
        from numpy import array
        for network in self.models[ID]:
            self.models[network][1] = \
                    array(self.models[network][1])
            self.models[network][2] = \
                    array(self.models[network][2])


    def add_model(self, ID, piece, model):
        self.models[ID][str(piece)][0] = model


    def get_model(self, ID, network):
        return self.models[ID][network][0]


    def get_models(self, ID):
        for network in self.models[ID]:
            yield self.models[ID][network] + [network]
        return StopIteration


    def add_performance(self, performance, ID, network):
        self.performances[ID][network].append(performance)


    def save_model(self, ID):
        for network in self.models[ID]:
            str_ID = ID.replace(' ', '_')
            ID = f'{str_ID}_{network}_network.h5'
            model = self.models[ID][network][0]
            model.save(f'{self.location}/brain/{ID}')

