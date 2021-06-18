'''
Data structure storing architecture of CnnBasic network
'''



class Architecture:
    def __init__(self, location):
        self.location = location
        self.configurations = dict()
        self.performances = dict()
        self.models = dict()
        self._load_models()


    def _load_configurations(self):
        from keras.optimizers import Adam, RMSprop, Nadam
        from keras.initializers import RandomUniform as RU, RandomNormal as RN
        from itertools import product
        conv_layer_infos = [
                {'5Slider Layer': (1, [16], [(4, 4)], ['relu'])},
                {'4Slider Layer': (1, [32], [(4, 4)], ['relu'])},
                {'3Slider Layer': (1, [16], [(3, 3)], ['relu'])},
                {'2Slider Layer': (1, [32], [(3, 3)], ['relu'])},
                ]
        dense_layer_infos = [
                {'128-12N Layer': (1, [[12], [128]], ['sigmoid'])},
                {'256-24N Layer': (1, [[24], [256]], ['sigmoid'])},
                {'512-48N Layer': (1, [[48], [512]], ['sigmoid'])},
                ]

        initializers = [
                {'Small Uniform Weights': RU(minval=0.0000001, maxval=0.000001)},
                #{'Large Uniform Weights': RU(minval=0.00001, maxval=0.0001)},
                #{'Small Normal Weights': RN(stddev=0.000001)},
                ]
        optimizers = [
                #{'RMSprop': RMSprop(learning_rate=0.0015)},
                #{'Adam': Adam(learning_rate=0.0015)},
                {'Nadam': Nadam()},
                ]
        loss_metrics = [
                {'Categorical-crossentropy': ('categorical_crossentropy', 'categorical_accuracy')},
                ]
        for info in product(dense_layer_infos, conv_layer_infos, initializers, optimizers, loss_metrics):
            dense_layer_info, conv_layer_info, initializer, optimizer, loss_metric = info
            d_name = list(dense_layer_info.keys())[0]
            c_name = list(conv_layer_info.keys())[0]
            i_name = list(initializer.keys())[0]
            o_name = list(optimizer.keys())[0]
            m_name = list(loss_metric.keys())[0]
            ID = f'{d_name} - {c_name} - {o_name} - {m_name}'
            self.models[ID] = {'S': None, 'K': None, 'Q': None, 'R': None,
                    'N': None, 'B': None, 'P': None}
            self.performances[ID] = {
                    'S':list(), 'K':list(), 'Q':list(), 'R':list(),
                    'N':list(), 'B':list(), 'P':list()}
            self.configurations[ID] = (dense_layer_info[d_name], conv_layer_info[c_name], initializer[i_name], optimizer[o_name], loss_metric[m_name])
        self.data = {'S' : [list(), list()], 'P' : [list(), list()],
                'B' : [list(), list()], 'N' : [list(), list()],
                'R' : [list(), list()], 'Q' : [list(), list()],
                'K' : [list(), list()],
                }


    def build_model(self, input_shape, output_shapes):
        from keras.models import Model
        from keras.layers import Input, Conv2D, Dense, Flatten
        self._load_configurations()
        inputs = Input(shape=input_shape)
        for ID in self.configurations:
            configuration = self.configurations[ID]
            d_layer_info, c_layer_info, initializer, optimizer, loss_metric = configuration
            d_num_layers, d_density, d_activation, = d_layer_info
            c_num_layers, c_density, c_sliders, c_activation, = c_layer_info
            for network in ['K', 'Q', 'R', 'N', 'B', 'P']:
                x = inputs
                for i in range(c_num_layers):
                    x = Conv2D(
                            c_density[i],
                            c_sliders[i],
                            activation=c_activation[i],
                            kernel_initializer=initializer)(x)
                x = Flatten()(x)
                for i in range(d_num_layers):
                    x = Dense(
                            d_density[1][i],
                            d_activation[i],
                            kernel_initializer=initializer)(x)
                outputs = Dense(output_shapes[0][0], output_shapes[0][1])(x)
                model = Model(inputs=inputs, outputs=outputs)
                model.compile(optimizer, loss_metric[0], [loss_metric[1]])
                self.models[ID][network] = model
            x = inputs
            for i in range(c_num_layers):
                x = Conv2D(
                        c_density[i],
                        c_sliders[i],
                        activation=c_activation[i],
                        kernel_initializer=initializer)(x)
            x = Flatten()(x)
            for i in range(d_num_layers):
                x = Dense(
                        d_density[0][i],
                        d_activation[i],
                        kernel_initializer=initializer)(x)
            outputs = Dense(output_shapes[1][0], output_shapes[1][1])(x)
            model = Model(inputs=inputs, outputs=outputs)
            model.compile(optimizer, loss_metric[0], [loss_metric[1]])
            self.models[ID]['S'] = model



    def _load_models(self):
        from os import listdir
        from keras.models import load_model
        brain_location = self.location + '/brain/'
        self.best_model = dict()
        for brain in listdir(brain_location):
            if 'best' in brain:
                ID = brain.split('best_')[1][0]
                self.best_model[ID] = load_model(brain_location + brain,
                        compile=False)


    def train(self, batch_size, epochs):
        from numpy import array
        for network in self.data:
            self.data[network][0] = \
                    array(self.data[network][0])
            self.data[network][1] = \
                    array(self.data[network][1])
        for ID in self.models:
            for network in self.models[ID]:
                model = self.models[ID][network]
                x, y = self.data[network]
                performance = model.fit(x, y,
                        epochs=epochs, batch_size=batch_size, validation_split=0.2,
                        verbose=0)
                self.performances[ID][network].append(performance)



    def _generate_best_model(self):
        from numpy import array
        candidates = {'S':list(), 'P':list(), 'B':list(), 'N':list(),
                'R':list(), 'Q':list(), 'K':list()}
        for ID in self.data:
            for model in self.performances:
                performances = list(map(lambda x: \
                    (x.history['categorical_accuracy'], x.history['val_categorical_accuracy']),
                    self.performances[model][ID]))
                candidates[ID].append((model, performances))
        for key in candidates:
            candidates[key] = sorted(candidates[key], key=lambda x: \
                    -x[1][-1][-1][-1])
        for key in candidates:
            name = candidates[key][0][0]
            self.best_model[key] = (name, self.models[name][key])
        with open(self.location + '/performances/performances.txt', 'a') as fp:
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
        for ID in self.best_model:
            piece, model = self.best_model[ID]
            model.save(f'{self.location}/brain/{piece}_best_{ID}.h5',
                    include_optimizer=False)


    def clear_data(self):
        for network in self.data:
            self.data[network][0] = list()
            self.data[network][1] = list()


    def add_data(self, network, x_data, y_data):
        self.data[network][0].append(x_data)
        self.data[network][1].append(y_data)


    def get_model(self, network):
        return self.best_model[network]


    def save_model(self):
        for ID in self.models:
            for network in self.models[ID]:
                model = self.models[ID][network]
                str_ID = ID.replace(' ', '_')
                str_ID = f'{str_ID}_{network}_network.h5'
                model.save(f'{self.location}/brain/{str_ID}',
                        include_optimizer=False)
        self._generate_best_model()
