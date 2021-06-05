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

from ai.models.cnn_basic.auxiliary_functions.functions import move_to_datapoint, boards_to_datapoints, moves_to_datapoints

LOSS = 'mean_squared_error'
LOSS_2 = 'categorical_crossentropy'

class CnnBasic(BaseModel):
    def __init__(self, game, location):
        super().__init__(game, location)

    def _load_model(self):
        from os import listdir
        from tensorflow.keras.models import load_model
        location = self.location + '/brain/'
        self.models = dict()
        for brain in listdir(location):
            if 'brain' in brain:
                model_ID = brain.split('_')[0]
                if model_ID == 'main':
                    self.model = load_model(location + brain)
                else:
                    self.models[model_ID] = load_model(location + brain)

    def _predict(self, board, is_white):
        from numpy import array
        piece_map = {'P': 0, 'B': 8, 'N': 10, 'R': 12, 'Q': 14, 'K':15}
        reverse_map = {0: 'P1', 1:'P2', 2:'P3', 3:'P4', 4:'P5', 5:'P6', 6:'P7',
                7:'P8', 8:'B1', 9:'B2', 10:'N1', 11:'N2', 12:'R1', 13:'R2',
                14:'Q1', 15:'K1'}
        dp = boards_to_datapoints([board])
        piece_moves = [0]*16
        piece_index = [0]*16
        for key in self.models:
            prediction = (self.models[key].predict(dp))[0]
            for i, val in enumerate(prediction):
                if val == max(prediction):
                    piece_moves[piece_map[key[0]] + int(key[1]) - 1] = val
                    piece_index[piece_map[key[0]] + int(key[1]) - 1] = i
                    break
        piece_moves = array(piece_moves)
        piece_moves = piece_moves.reshape((1, 16))
        prediction = (self.model.predict([dp, piece_moves]))[0]
        for i, val in enumerate(prediction):
            if val == max(prediction):
                piece = i
                break
        move_index = piece_index[piece]
        piece_ID = reverse_map[piece]
        my_pieces = board.white_pieces if is_white else board.black_pieces
        for piece in my_pieces:
            ID = piece.ID if piece.value != 9 else 1
            if str(piece).upper() + str(ID) == piece_ID:
                source = piece.location[0]*10 + piece.location[1]
                destination = piece.move_IDs[move_index](piece.location)
        return source, destination


    def _build_model(self):
        if hasattr(self, 'model'):
            return
        from tensorflow.keras.models import Model
        from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, \
            Concatenate, Lambda, Reshape, MaxPooling2D, Dropout
        from tensorflow.keras.optimizers import SGD

        self.game.__init__()
        self.models = dict()
        for piece in self.game.board.white_pieces:
            location = str(piece).upper() + str(piece.ID) \
                    if not piece.value == 9 else str(piece).upper() + str(1)
            inputs = Input(shape=(8, 8, 5))
            x = Conv2D(32, (4, 4), activation='relu')(inputs)
            x = MaxPooling2D()(x)
            x = Conv2D(16, (2, 2), activation='relu')(x)
            x = Flatten()(x)
            x = Dense(40, activation='relu')(x)
            outputs = Dense(len(piece.move_IDs), activation='sigmoid')(x)
            opt = SGD(lr=0.05, momentum=0.9)
            model = Model(inputs, outputs)
            model.compile(optimizer=opt, loss=LOSS,
                    metrics=[LOSS])
            self.models[location] = [model, list(), list()]
        inputs_1 = Input(shape=(8, 8, 5))
        x = Conv2D(32, (4, 4), activation='relu')(inputs_1)
        x = MaxPooling2D()(x)
        x = Conv2D(16, (2, 2), activation='relu')(x)
        x = Flatten()(x)
        x = Dense(16, activation='relu')(x)

        inputs_2 = Input(shape=(16,))
        x = Concatenate()([x, inputs_2])
        x = Dense(16, activation='relu')(x)
        x = Flatten()(x)
        x = Dense(32, activation='relu')(x)
        x = Dropout(0.2)(x)
        x = Dense(16, activation='relu')(x)
        outputs = Dense(16, activation='softmax')(x)
        opt = SGD(lr=0.05, momentum=0.9)
        model = Model(inputs=[inputs_1, inputs_2], outputs=outputs)
        model.compile(optimizer=opt, loss=LOSS_2,
                metrics=[LOSS_2])
        self.model = [model, list([list(), list()]), list()]


    def _train_model(self):
        from sklearn.model_selection import train_test_split
        from numpy import array
        from time import time
        start = time()
        num_datapoints = 100
        print(f'Begin downloading data.')
        for i, data in enumerate(self.datapoints(num_datapoints)):
            '''
            if i % (num_datapoints//100) == 0:
                print(f'{i//(num_datapoints//100)}% downloading')
            '''
            boards, moves = data
            x_data = boards_to_datapoints(boards)
            white_turn = True
            for i in range(len(boards)):
                my_pieces = boards[i].white_pieces if white_turn \
                        else boards[i].black_pieces
                for piece in my_pieces:
                    ID = piece.ID if piece.value != 9 else 1
                    key = str(piece).upper() + str(ID)
                    model = self.models[key]
                    y = move_to_datapoint(boards[i], piece)
                    model[1].append(x_data[i])
                    model[2].append(y)
                white_turn = not(white_turn)
        for key in self.models:
            x_data, y_data = self.models[key][1], self.models[key][2]
            x_data, y_data = array(x_data), array(y_data)
            x_data = x_data.reshape((x_data.shape[0], 8, 8, 5))
            y_data = y_data.reshape((y_data.shape[0], y_data.shape[1]))
            for i in range(5):
                x_val = max(max(x_data[:,:,:,i:i+1].reshape(-1,)), 1)
                x_data[:,:,:,i:i+1] = x_data[:,:,:,i:i+1] / x_val
            for i in range(y_data.shape[1]):
                y_val = max(max(y_data[:,i:i+1].reshape(-1,)), 1)
                y_data[:,i:i+1] = y_data[:,i:i+1] / y_val
            self.models[key][1] = x_data
            self.models[key][2] = y_data
        # Make final models numpy arrays
        print(f'Done downloading. Took {time()-start}s')
        start = time()
        x_data, y_data = array(x_data), array(y_data)
        x_data = x_data.reshape((x_data.shape[0], 8, 8, 5))
        print(f'Begin learning over {x_data.shape[0]} datapoints')
        self.performances = dict()
        for key in self.models:
            model = self.models[key]
            print(f'Learning model for: {key}')
            performance = model[0].fit(model[1], model[2],
                    epochs=30, batch_size=32, validation_split=0.2, verbose=0)
            self.performances[key] = performance
        print(f'Done learning. Took {str(time()-start)[0:5]}s')
        print(f'Main Network: Begin downloading data.')
        piece_map = {'P': 0, 'B': 8, 'N': 10, 'R': 12, 'Q': 14, 'K':15}
        for i, data in enumerate(self.datapoints(num_datapoints)):
            '''
            if i % (num_datapoints//100) == 0:
                print(f'Main Network: {i//(num_datapoints//100)}% downloading')
            '''
            boards, moves = data
            x_data = boards_to_datapoints(boards)
            x = [0] * len(boards)
            y_info = [0] * len(boards)
            for i in range(len(boards)):
                x[i] = array([0] * 16)
                y_info[i] = array([0]*16)
            for piece in boards[i].white_pieces:
                ID = piece.ID if piece.value != 9 else 1
                model = self.models[str(piece) + str(ID)][0]
                get_move = model.predict(x_data)
                for i, prediction in enumerate(get_move):
                    for j, val in enumerate(prediction):
                        if val == max(prediction):
                            x[i][piece_map[str(piece)] + ID - 1] = val
                            y_info[i][piece_map[str(piece)] + ID - 1] = j
                            break
            x_data = list(x_data)
            y, bad_indicies = moves_to_datapoints(boards, moves, y_info)
            for index in bad_indicies[::-1]:
                del x[index]
                del x_data[index]
            self.model[1][0].extend(x_data)
            self.model[1][1].extend(x)
            self.model[2].extend(y)
        x_1 = self.model[1][0]
        x_1 = array(x_1)
        x_1 = x_1.reshape((x_1.shape[0], 8, 8, 5))
        for i in range(5):
            x_val = max(max(x_1[:,:,:,i:i+1].reshape(-1,)), 1)
            x_1[:,:,:,i:i+1] = x_1[:,:,:,i:i+1] / x_val

        x_data = self.model[1][1]
        y_data = self.model[2]
        x_data, y_data = array(x_data), array(y_data)
        x_data = x_data.reshape((x_data.shape[0], 16))
        y_data = y_data.reshape((y_data.shape[0], 16))
        for i in range(x_data.shape[0]):
            val = max(max(x_data[i:i+1,:].reshape((-1,))), 1)
            x_data[i:i+1,:] = x_data[i:i+1,:] / val
        self.model[1][0] = x_1
        self.model[1][1] = x_data
        self.model[2] = y_data

        print(f'Main Network: Done downloading. Took {time()-start}s')

        print(f'Main Network: Begin learning over {self.model[2].shape[0]} datapoints')
        model = self.model
        performance = model[0].fit([model[1][0], model[1][1]], model[2],
                epochs=100, batch_size=32, validation_split=0.2, verbose=1)
        self.performances['main'] = performance

        print(f'Main Network: Done learning. Took {str(time()-start)[0:5]}s')

        for key in self.models:
            self.models[key][0].save(f'{self.location}/brain/{key}_brain.h5')
        self.model[0].save(f'{self.location}/brain/main_brain.h5')



    def _evaluate_model(self):
        from matplotlib import pyplot
        from numpy import mean, std
        fig, axs = pyplot.subplots(4, 4)
        fig.suptitle('Piece Network Accuracy')
        it = iter(self.performances.keys())
        for i in range(4):
            for j in range(4):
                performance = next(it)
                if performance == 'main':
                    performance = next(it)
                model = self.performances[performance]
                axs[i, j].set_title(f'{performance}')
                axs[i, j].plot(model.history[LOSS],
                        color='blue', label='train')
                axs[i, j].plot(model.history['val_' + LOSS],
                        color='orange', label='test')
        for ax in axs.flat:
            ax.set(xlabel='Epoch', ylabel='Accuracy')
        for ax in axs.flat:
            ax.label_outer()
        pyplot.legend()
        pyplot.show()
        fig, axs = pyplot.subplots()
        axs.set_title('Main Network')
        pyplot.xlabel('Epoch')
        pyplot.ylabel('Accuracy')
        axs.plot(self.performances['main'].history[LOSS_2],
                color='blue', label='train')
        axs.plot(self.performances['main'].history['val_' + LOSS_2],
                color='orange', label='test')
        pyplot.legend()
        pyplot.show()

