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
        # self._load_model()


    def _load_configurations(self):
        from keras.optimizers import Adam, RMSprop, Adagrad, Adadelta, Adamax, Nadam, Ftrl
        from keras.initializers import RandomUniform as RU,\
                RandomNormal as RN
        from itertools import product
        self.colors = [('midnightblue', 'darkorange'),('mediumblue', 'burlywood'),
                ('blue', 'navajowhite'), ('slateblue', 'papayawhip'),
                ('mediumpurple', 'orange'), ('indigo', 'floralwhite'),
                ('darkviolet', 'darkgoldenrod'), ('violet', 'gold'),
                ('fuchsia', 'lemonchiffon'), ('orchid', 'darkkhaki'),
                ('hotpink', 'lightyellow'), ('pink', 'olive'),
                ('lightpink', 'olivedrab'), ('forestgreen', 'lightcoral'),
                ('limegreen', 'brown'), ('green', 'maroon'),
                ('seagreen', 'red'), ('mediumseagreen', 'salmon'),
                ('aquamarine', 'coral'), ('turquoise', 'orangered'),
                ('mediumturquoise', 'sienna'), ('lightcyan', 'chocolate'),
                ('teal', 'peachpuff'), ('aqua', 'linen'), ('cyan', 'slategrey'),
                ('deepskyblue', 'dimgray'), ('lightblue', 'silver'),
                ]
        layer_infos = [
                #{'1 Layer': (1, [128], [(4, 4))], ['relu'])},
                #{'2 DLayers': (2, [64, 16], [(4, 4), (3, 3)], ['relu']*2)},
                {'2 Layers': (2, [32, 128], [(4, 4), (3, 3)], ['relu']*2)},
                {'3 Layers': (3, [8, 16, 32], [(4, 4), (3, 3), (2, 2)], ['relu']*3)},
                ]
        initializers = [
                #{'Small Uniform Weights': RU(minval=0.00000001, maxval=0.0000001)},
                #{'Large Uniform Weights': RU(minval=0.00001, maxval=0.0001)},
                {'Small Normal Weights': RN(mean=0, stddev=0.0000001)},
                ]
        optimizers = [
                {'RMSprop': RMSprop(learning_rate=0.000001)},
                {'Adam': Adam(learning_rate=0.000001)},
                {'Adagrad': Adagrad(learning_rate=0.000001)},
                {'Adadelta': Adadelta(learning_rate=0.000001)},
                {'Adamax': Adamax(learning_rate=0.000001)},
                {'Nadam': Nadam(learning_rate=0.000001)},
                {'Ftrl': Ftrl(learning_rate=0.000001)},
                ]
        loss_metrics = [
                {'Categorical-crossentropy': 'categorical_crossentropy'},
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
        from keras.models import load_model
        from keras.optimizers import Adam, RMSprop
        from keras.initializers import RandomUniform, RandomNormal
        brain_location = self.location + '/brain/'
        for brain in listdir(brain_location):
            if '.h5' in brain:
                name = brain.split('_')
                ID = ' '.join(name[0:10])
                network = name[10]
                self.models[ID][network] = load_model(brain_location + brain)


    def built(self):
        return bool(self.models[list(self.models.keys())[0]]['S'])


    def generate_best_model(self):
        from numpy import array
        candidates = {'S':list(), 'P':list(), 'B':list(), 'N':list(),
                'R':list(), 'Q':list(), 'K':list()}
        for ID in self.data:
            for model in self.performances:
                performances = list(map(lambda x: \
                    (x.history['loss'], x.history['val_loss']),
                    self.performances[model][ID]))
                candidates[ID].append((model, performances))
        for key in candidates:
            candidates[key] = sorted(candidates[key], key=lambda x: \
                    x[1][-1][-1][-1])
        with open(self.location + '/performances/performance.txt', 'w') as fp:
            for key in candidates:
                output = f'\nPerformances for {key} network\n'
                for perf in candidates[key]:
                    name = perf[0]
                    performance = perf[1][-1]
                    train = array(performance[0][1::2]).round(3)
                    test = array(performance[1][1::2]).round(3)
                    output += f'{str(test)}:Test, {str(train)}:Train, {name[0:-15].replace(" ", "")}\n'
                output += '\n\n'
                fp.write(output)


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

