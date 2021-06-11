'''
Data structure storing architecture of CnnBasic network
'''



class Architecture:
    def __init__(self, location):
        self.location = location
        self.configurations = dict()
        self.performances = dict()
        self.models = dict()
        self._load_configurations()
        self._load_model()


    def _load_configurations(self):
        from tensorflow.keras.optimizers import SGD, Adam, RMSprop
        from tensorflow.keras.initializers import RandomUniform as RU,\
                RandomNormal as RN
        from itertools import product
        layer_infos = [
#                {'1 Shallow Layer': (1, [16], [(4, 4)], ['relu'])},
#                {'1 Dense Layer': (1, [32], [(4, 4)], ['relu'])},
#                {'2 Shallow Layers': (2, [16, 32], [(4, 4), (3, 3)], ['relu']*2)},
                {'2 Dense Layers': (2, [32, 64], [(4, 4), (3, 3)], ['relu']*2)},
#                {'3 Shallow Layers': (3, [16, 32, 64], [(4, 4), (3, 3), (2, 2)], ['relu']*3)},
                {'3 Dense Layers': (3, [32, 64, 128], [(3, 3), (2, 2), (1, 1)], ['relu']*3)},
                ]
        initializers = [
#                {'Small Uniform Weights': RU(minval=0.0000001, maxval=0.000001)},
                {'Large Uniform Weights': RU(minval=0.00001, maxval=0.0001)},
#                {'Small Normal Weights': RN(mean=0, stddev=0.0000001)},
                {'Large Normal Weights': RN(mean=0, stddev=0.00001)},
                ]
        optimizers = [
                {'RMSprop': RMSprop()},
#                {'SGD': SGD(learning_rate=0.001)},
#                {'Adam': Adam()},
                ]
        loss_metrics = [
                {'Categorical-crossentropy': 'categorical_crossentropy'},
#                {'Mean-squared-error': 'mean_squared_error'},
                ]
        for info in product(layer_infos, initializers, optimizers, loss_metrics):
            layer_info, initializer, optimizer, loss_metric = info
            l_name = list(layer_info.keys())[0]
            i_name = list(initializer.keys())[0]
            o_name = list(optimizer.keys())[0]
            m_name = list(loss_metric.keys())[0]
            ID = f'{l_name} - {i_name} - {o_name} - {m_name}'
            self.models[ID] = {'S': None, 'K': None, 'Q': None, 'R': None,
                    'N': None, 'B': None, 'P': None}
            self.performances[ID] = {
                    'S':list(), 'K':list(), 'Q':list(), 'R':list(),
                    'N':list(), 'B':list(), 'P':list()}
            self.configurations[ID] = (layer_info[l_name], initializer[i_name],
                    optimizer[o_name], loss_metric[m_name])
        self.data = {'S' : [list(), list()], 'P' : [list(), list()],
                'B' : [list(), list()], 'N' : [list(), list()],
                'R' : [list(), list()], 'Q' : [list(), list()],
                'K' : [list(), list()],
                }


    def _load_model(self):
        from os import listdir
        from tensorflow.keras.models import load_model
        from tensorflow.keras.optimizers import SGD, Adam, RMSprop
        from tensorflow.keras.initializers import RandomUniform, RandomNormal
        brain_location = self.location + '/brain/'
        for brain in listdir(brain_location):
            if '.h5' in brain:
                name = brain.split('_')
                ID = ' '.join(name[0:11])
                network = name[11]
                self.models[ID][network] = load_model(brain_location + brain)


    def built(self):
        return bool(self.models[list(self.models.keys())[0]]['S'])


    def generate_best_model(self):
        '''
        Look at performances for each network and pick best one
        '''
        self.best_model = {'S':None, 'K': None, 'Q':None, 'R':None, 'N':None,
                'B':None, 'P':None}
        pass


    def clear_data(self):
        for network in self.data:
            self.data[network][0] = list()
            self.data[network][1] = list()


    def add_data(self, network, x_data, y_data):
        self.data[network][0].append(x_data)
        self.data[network][1].append(y_data)


    def prepare_data(self):
        from numpy import array
        for network in self.data:
            self.data[network][0] = \
                    array(self.data[network][0])
            self.data[network][1] = \
                    array(self.data[network][1])


    def add_model(self, ID, piece, model):
        self.models[ID][str(piece)] = model


    def get_model(self, network):
        return self.best_model[network]


    def get_models(self):
        for ID in self.models:
            for network in self.models[ID]:
                yield (self.models[ID][network],
                        self.data[network][0],
                        self.data[network][1],
                        ID,
                        network)
        return StopIteration


    def add_performance(self, performance, ID, network):
        self.performances[ID][network].append(performance)


    def save_model(self, ID):
        for network in self.models[ID]:
            model = self.models[ID][network]
            str_ID = ID.replace(' ', '_')
            str_ID = f'{str_ID}_{network}_network.h5'
            model.save(f'{self.location}/brain/{str_ID}')

