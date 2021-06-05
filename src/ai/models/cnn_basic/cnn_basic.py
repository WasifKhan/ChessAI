'''
AI Implemented Using A Basic Convolutional Neural Network

self._predict(board, is_white)
self._load_model()
self._build_model()
self._train_model()
self._evaluate_model()
self._move_to_datapoint(move)
self._board_to_datapoint(board, is_white)
'''

from ai.models.base_model import BaseModel
from ai.models.cnn_basic.auxiliary_functions.functions import boards_to_datapoints, moves_to_datapoints
from ai.models.cnn_basic.moves import MOVES as MOVES

LOSS = 'binary_crossentropy'
ACTIVATION = 'sigmoid'

class CnnBasic(BaseModel):
    def __init__(self, game, location):
        from tensorflow.keras.models import load_model
        from os import listdir
        super().__init__(game, location)
        location = self.location + '/brain/'
        self.models = list()
        self.names = list()
        for brain in listdir(location):
            if 'brain' in brain:
                self.models.append(load_model(location + brain))

    def _predict(self, board, is_white):
        from numpy import array
        dp = boards_to_datapoints([board], False)
        predictions = dict()
        for model in self.models:
            prediction = model.predict(array(dp))[0]
            for i, val in enumerate(prediction):
                if val == max(prediction):
                    move = i
            for key in MOVES:
                if MOVES[key] == move:
                    move_ID = key
            piece_ID, move_index = move_ID[0:2], int(move_ID[2])
            my_pieces = board.white_pieces if is_white else board.black_pieces
            source = None
            for piece in my_pieces:
                ID = piece.ID if piece.value != 9 else 1
                if str(piece).upper() + str(ID) == piece_ID:
                    source = piece.location[0]*10 + piece.location[1]
                    destination = piece.move_IDs[move_index](piece.location)
                if source and board.is_valid_move(board[source],
                        (destination//10, destination%10)):
                    if (source, destination) not in  predictions:
                        predictions[(source, destination)] = 1
                    else:
                        predictions[(source, destination)] += 1
        max_vote = None
        move = None
        for key in predictions:
            if not max_vote:
                max_vote = predictions[key]
                move = key
            elif predictions[key] > max_vote:
                max_vote = predictions[key]
                move = key
        return move


    def _build_model(self):
        if self.models:
            return
        from tensorflow.keras.models import Model
        from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, \
            Concatenate, Lambda, Reshape, MaxPooling2D, Dropout
        from tensorflow.keras.optimizers import SGD
        self.names = list()
        inputs = Input(shape=(8, 8, 5))
        x = Conv2D(32, (4, 4), activation='relu')(inputs)
        x = MaxPooling2D()(x)
        x = Conv2D(64, (2, 2), activation='relu')(x)
        x = Flatten()(x)
        x = Dense(300, activation='relu')(x)
        outputs = Dense(142, activation=ACTIVATION)(x)
        opt = SGD(lr=0.01, momentum=0.8)
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=opt, loss=LOSS, metrics=[LOSS])
        self.names.append('Conv2d w/ pool+300dense')
        self.models.append(model)

        inputs = Input(shape=(8, 8, 5))
        x = Conv2D(16, (4, 4), activation='relu')(inputs)
        x = MaxPooling2D()(x)
        x = Conv2D(32, (2, 2), activation='relu')(x)
        x = Flatten()(x)
        outputs = Dense(142, activation=ACTIVATION)(x)
        opt = SGD(lr=0.01, momentum=0.8)
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=opt, loss=LOSS, metrics=[LOSS])
        self.names.append('shallow Conv2d w/ pool')
        self.models.append(model)

        inputs = Input(shape=(8, 8, 5))
        x = Dense(64, activation='relu')(inputs)
        x = Flatten()(x)
        x = Dense(300, activation='relu')(x)
        outputs = Dense(142, activation=ACTIVATION)(x)
        opt = SGD(lr=0.01, momentum=0.8)
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=opt, loss=LOSS, metrics=[LOSS])
        self.names.append('ffnn multi-layer')
        self.models.append(model)

        inputs = Input(shape=(8, 8, 5))
        x = Dense(64, activation='relu')(inputs)
        x = Flatten()(x)
        x = Dense(300, activation='relu')(x)
        outputs = Dense(142, activation=ACTIVATION)(x)
        opt = SGD(lr=0.001, momentum=0.6)
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=opt, loss=LOSS, metrics=[LOSS])
        self.names.append('ffnn multilayer, low learning rate/momentum')
        self.models.append(model)


    def _train_model(self):
        from numpy import array
        from time import time
        start = time()
        num_datapoints = 10000
        x = list()
        y = list()
        self.logger.error('test error')
        my_data = self.get_data()
        self.logger.info(f'Begin downloading data.')
        for i, data in enumerate(self.datapoints(num_datapoints)):
            if i >= 100 and i % (num_datapoints//100) == 0:
                self.logger.log(f'{i//(num_datapoints//100)}% downloading')
            boards, moves = data
            x_data = boards_to_datapoints(boards)
            y_data, bad_indicies = moves_to_datapoints(boards, my_data)
            for index in bad_indicies[::-1]:
                del x_data[index]
                del y_data[index]
            x.extend(x_data)
            y.extend(y_data)
        x, y = array(x), array(y)
        x = x.reshape((x.shape[0], 8, 8, 5))
        y = y.reshape((y.shape[0], 142))
        for i in range(5):
            x_val = max(max(x[:,:,:,i:i+1].reshape(-1,)), 1)
            x[:,:,:,i:i+1] = x[:,:,:,i:i+1] / x_val
        x = x.reshape((x.shape[0], 8, 8, 5))
        self.logger.info(f'Done downloading. Took {str(time()-start)[0:5]}s')
        self.logger.info(f'Begin learning over {x.shape[0]} datapoints')
        start = time()
        self.performances = list()
        for i, model in enumerate(self.models):
            self.performances.append(model.fit(x, y,
                epochs=10, batch_size=32, validation_split=0.2, verbose=0))
            model.save(f'{self.location}/brain/brain_{i}.h5')
        self.logger.info(f'Done learning. Took {str(time()-start)[0:5]}s')


    def _evaluate_model(self):
        from matplotlib import pyplot
        from numpy import mean, std
        fig, axs = pyplot.subplots(4)
        fig.suptitle('Network Performances')
        colors = ['blue', 'orange', 'red', 'green']
        for i, performance in enumerate(self.performances):
            axs[i].set_title(f'{self.names[i]}')
            axs[i].plot(performance.history[LOSS],
                    color=colors[0], label=f'train accuracy')
            axs[i].plot(performance.history['val_' + LOSS],
                    color=colors[1], label='test accuracy')
            axs[i].plot(performance.history['loss'],
                    color=colors[2], label=f'train_loss')
            axs[i].plot(performance.history['val_loss'],
                    color=colors[3], label=f'test loss')
        for ax in axs.flat:
            ax.set(xlabel='Epoch', ylabel='Accuracy')
        for ax in axs.flat:
            ax.label_outer()
        pyplot.legend()
        pyplot.show()
