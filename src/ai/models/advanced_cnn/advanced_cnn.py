'''
AI Implemented Using Several Convolutional Neural Networks
'''

from ai.models.base_model import BaseModel



class AdvancedCnn(BaseModel):
    def __init__(self, game, location):
        super().__init__(game, location)

    def _load_model(self):
        from tensorflow.keras.models import load_model
        from os import listdir
        self.models = dict()
        self.models['get_move'] = dict()
        self.models['should_move'] = dict()
        self.models['vote_best_move'] = None
        for brain in listdir(self.location + '/brain/'):
            if 'brain' not in brain:
                continue
            model, _, piece, _ = brain.split('_')
            if model == 'get':
                self.models['get_move'][piece] = load_model(self.location + '/brain/' + brain)
            elif model == 'should':
                self.models['should_move'][piece] = load_model(self.location + '/brain/' + brain)
            elif model == 'vote':
                self.models['vote_best_move'] = load_model(self.location + '/brain/' + brain)

    def _train(self):
        self.build_model()
        self.train_model()
        self.evaluate_model()

    def _predict(self, board, is_white):
        from numpy import array
        piece_map = {'P': 0, 'B': 8, 'N': 10, 'R': 12, 'Q': 14, 'K':15}
        my_pieces = board.white_pieces if is_white else board.black_pieces
        x_data = self._boards_to_datapoints([board])
        datapoint = [0] * 16
        board_datapoint = [0] * 16
        for i in range(16):
            board_datapoint[i] = [0]*6
        for piece in my_pieces:
            model = self.models['should_move'][str(piece).upper() + str(piece.ID)]
            should_move = model.predict(x_data)
            model = self.models['get_move'][str(piece).upper() + str(piece.ID)]
            get_move = model.predict(x_data)
            if round(should_move[0][0]) == 1:
                for i, val in enumerate(get_move[0]):
                    if val == max(get_move[0]):
                        datapoint[piece_map[str(piece).upper()] + piece.ID - 1] = i
                        break
            piece.compute_info(board)
            ID = piece.ID if piece.is_white is not None else 0
            value = piece.value if piece.is_white == is_white \
                    else piece.value * -1
            piece_info = [ID/10, value/10, piece.defends/10,
                    piece.threats/10, piece.threatens/10,
                    piece.num_moves/10]
            piece_info = array(piece_info)
            board_datapoint[piece_map[str(piece).upper()] + piece.ID - 1] = piece_info
        datapoint = array(datapoint)
        datapoint = datapoint.reshape((1, 16, 1))
        board_datapoint = array(board_datapoint)
        board_datapoint = board_datapoint.reshape((1, 16, 6))
        model = self.models['vote_best_move']
        prediction = model.predict([board_datapoint, datapoint])

        for i, val in enumerate(prediction[0]):
            if val == max(prediction[0]):
                move = datapoint[0][i]
                print(move)
                move = int(move)
                for piece in my_pieces:
                    if piece_map[str(piece).upper()] + piece.ID - 1 == i:
                            move = piece.move_IDs[move](piece.location)
                            return piece.location[0]*10+piece.location[1], move
        print(f'move not found')
        return None

    def build_model(self):
        from tensorflow.keras.models import Model
        from tensorflow.keras.layers import Input, Conv1D, Conv2D, Dense, Flatten, \
            Concatenate, Lambda, Reshape, MaxPooling2D, Dropout
        from tensorflow.keras.optimizers import SGD
        self.game.__init__()
        self.models = dict()
        self.models['should_move'] = dict()
        self.models['get_move'] = dict()
        pieces = self.game.board.white_pieces
        for piece in pieces:
            location = str(piece).upper() + str(piece.ID) \
                    if not piece.value == 9 else str(piece).upper() + str(1)
            inputs = Input(shape=(8, 8, 6))
            x = Conv2D(16, (4, 4), activation='relu')(inputs)
            x = Conv2D(8, (2, 2), activation='relu')(x)
            x = Flatten()(x)
            x = Dense(20, activation='relu')(x)
            outputs = Dense(1, activation='sigmoid')(x)
            opt = SGD(lr=0.1, momentum=0.9)
            model = Model(inputs, outputs)
            model.compile(optimizer=opt, loss='binary_crossentropy',
                            metrics=['binary_accuracy'])
            self.models['should_move'][location] = [model, list(), list()]

            inputs = Input(shape=(8, 8, 6))
            x = Conv2D(32, (4, 4), activation='relu')(inputs)
            x = Conv2D(16, (2, 2), activation='relu')(x)
            x = Flatten()(x)
            x = Dense(64, activation='relu')(x)
            x = Dropout(0.2)(x)
            x = Dense(32, activation='relu')(x)
            x = Dropout(0.2)(x)
            outputs = Dense(len(piece.move_IDs), activation='sigmoid')(x)
            opt = SGD(lr=0.05, momentum=0.8)
            model = Model(inputs, outputs)
            model.compile(optimizer=opt, loss='binary_crossentropy',
                            metrics=['binary_accuracy'])
            self.models['get_move'][location] = [model, list(), list()]
        inputs1 = Input(shape=(16,6))
        inputs2 = Input(shape=(16,1))
        x = Dense(1, activation='relu')(inputs1)
        x = Concatenate()([x, inputs2])
        x = Dense(1, activation='relu')(x)
        x = Flatten()(x)
        x = Dense(64, activation='relu')(x)
        x = Dropout(0.2)(x)
        outputs = Dense(16, activation='softmax')(x)
        opt = SGD(lr=0.05, momentum=0.8)
        model = Model(inputs=[inputs1, inputs2], outputs=outputs)
        model.compile(optimizer=opt, loss='categorical_crossentropy',
                        metrics=['categorical_accuracy'])
        self.models['vote_best_move'] = [model, list([list(), list()]), list()]


    def train_model(self):
        from sklearn.model_selection import train_test_split
        from numpy import array
        from time import time
        start = time()
        num_datapoints = 500
        print(f'Begin downloading data.')
        for i, data in enumerate(self.datapoints(num_datapoints)):
            if i % (num_datapoints//100) == 0:
                print(f'{i//(num_datapoints//100)}% downloading')
            boards, moves = data
            self.game.__init__()
            x_data = self._boards_to_datapoints(boards)
            for i in range(len(boards)):
                my_pieces = boards[i].white_pieces if self.game.white_turn \
                        else boards[i].black_pieces
                piece = boards[i][moves[i][0]]
                ID = piece.ID if not piece.value == 9 else 1
                y = self._move_to_datapoint(boards[i], piece)
                self.game.move(*moves[i])
                y[int(self.game.board.move_ID[-1])] = 1
                y = array(y)
                for key in self.models['should_move']:
                    self.models['should_move'][key][1].append(x_data[i])
                    if key == str(piece).upper() + str(ID):
                        self.models['should_move'][key][2].append(1)
                    else:
                        self.models['should_move'][key][2].append(0)
                self.models['get_move'][str(piece).upper() + str(ID)][1].append(x_data[i])
                self.models['get_move'][str(piece).upper() + str(ID)][2].append(y)
        for key in self.models['should_move']:
            x_data = self.models['should_move'][key][1]
            y_data = self.models['should_move'][key][2]
            x_data, y_data = array(x_data), array(y_data)
            x_data = x_data.reshape((x_data.shape[0], 8, 8, 6))
            self.models['should_move'][key][1] = x_data
            self.models['should_move'][key][2] = y_data
        for key in self.models['get_move']:
            x_data = self.models['get_move'][key][1]
            y_data = self.models['get_move'][key][2]
            x_data, y_data = array(x_data), array(y_data)
            x_data = x_data.reshape((x_data.shape[0], 8, 8, 6))
            self.models['get_move'][key][1] = x_data
            self.models['get_move'][key][2] = y_data
        print(f'Done downloading. Took {time()-start}s')

        start = time()
        self.performances = dict()
        self.performances['should_move'] = dict()
        self.performances['get_move'] = dict()
        print(f'Begin learning over {self.models["should_move"][key][1].shape[0]*2} datapoints')
        for key in self.models['should_move']:
            print(f'Learning model for: {key}')
            model = self.models['should_move'][key]
            performance = model[0].fit(model[1], model[2],
                    epochs=10, batch_size=32, validation_split=0.2, verbose=0)
            self.performances['should_move'][key] = performance
        for key in self.models['get_move']:
            print(f'Learning model for: {key}')
            model = self.models['get_move'][key]
            performance = model[0].fit(model[1], model[2],
                    epochs=20, batch_size=32, validation_split=0.2, verbose=0)
            self.performances['get_move'][key] = performance

        piece_map = {'P': 0, 'B': 8, 'N': 10, 'R': 12, 'Q': 14, 'K':15}
        print(f'Done learning. Took {str(time()-start)[0:5]}s')

        print(f'Main Network: Begin downloading data.')
        for i, data in enumerate(self.datapoints(num_datapoints)):
            if i % (num_datapoints//100) == 0:
                print(f'Main Network: {i//(num_datapoints//100)}% downloading')
            boards, moves = data
            x_data = self._boards_to_datapoints(boards)
            for piece in boards[0].white_pieces:
                model = self.models['should_move'][str(piece) + str(piece.ID)][0]
                should_move = model.predict(x_data)
                model = self.models['get_move'][str(piece) + str(piece.ID)][0]
                get_move = model.predict(x_data)
            x2 = [0] * len(should_move)
            for i, prediction in enumerate(should_move):
                datapoint = [0] * 16
                if round(prediction[0]) == 1:
                    move = get_move[i]
                    for j, val in enumerate(move):
                        if val == max(move):
                            datapoint[piece_map[str(piece).upper()] + piece.ID - 1 ] = j
                            break
                datapoint = array(datapoint)
                x2[i] = datapoint
            x1, y = self._pieces_to_datapoints(boards, moves)
            self.models['vote_best_move'][1][0].extend(x1)
            self.models['vote_best_move'][1][1].extend(x2)
            self.models['vote_best_move'][2].extend(y)
        x_data_1 = self.models['vote_best_move'][1][0]
        x_data_2 = self.models['vote_best_move'][1][1]
        y_data = self.models['vote_best_move'][2]
        x_data_1, x_data_2, y_data = array(x_data_1), array(x_data_2), array(y_data)
        x_data_1 = x_data_1.reshape((x_data_1.shape[0], 16, 6))
        self.models['vote_best_move'][1][0] = x_data_1
        self.models['vote_best_move'][1][1] = x_data_2
        self.models['vote_best_move'][2] = y_data

        print(f'Main Network: Done downloading. Took {time()-start}s')

        print(f'Main Network: Begin learning over\
        {self.models["vote_best_move"][2].shape[0]} datapoints')
        model = self.models['vote_best_move']
        performance = model[0].fit([model[1][0], model[1][1]], model[2],
                epochs=50, batch_size=32, validation_split=0.2, verbose=0)
        self.performances['vote_best_move'] = performance

        print(f'Main Network: Done learning. Took {str(time()-start)[0:5]}s')

        for key in self.models['should_move']:
            self.models['should_move'][key][0].save(f'{self.location}/brain/should_move_{key}_brain.h5')
        for key in self.models['get_move']:
            self.models['get_move'][key][0].save(f'{self.location}/brain/get_move_{key}_brain.h5')
        self.models['vote_best_move'][0].save(f'{self.location}/brain/vote_best_move_brain.h5')


    def evaluate_model(self):
        from matplotlib import pyplot
        from numpy import mean, std
        fig, axs = pyplot.subplots(4, 4)
        fig.suptitle('Should Move Networks')
        it = iter(self.performances['should_move'])
        for i in range(4):
            for j in range(4):
                performance = next(it)
                model = self.performances['should_move'][performance]
                axs[i, j].set_title(f'{performance}')
                axs[i, j].plot(model.history['binary_accuracy'],
                        color='blue', label='train')
                axs[i, j].plot(model.history['val_binary_accuracy'],
                        color='orange', label='test')
        for ax in axs.flat:
            ax.set(xlabel='Epoch', ylabel='Accuracy')
        for ax in axs.flat:
            ax.label_outer()
        pyplot.legend()
        pyplot.show()
        fig, axs = pyplot.subplots(4, 4)
        fig.suptitle('Get Move Networks')
        it = iter(self.performances['get_move'])
        for i in range(4):
            for j in range(4):
                performance = next(it)
                model = self.performances['get_move'][performance]
                axs[i, j].set_title(f'{performance}')
                axs[i, j].plot(model.history['binary_accuracy'],
                        color='blue', label='train')
                axs[i, j].plot(model.history['val_binary_accuracy'],
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
        axs.plot(self.performances['vote_best_move'].history['categorical_accuracy'],
                color='blue', label='train')
        axs.plot(self.performances['vote_best_move'].history['val_categorical_accuracy'],
                color='orange', label='test')
        pyplot.legend()
        pyplot.show()

    def _pieces_to_datapoints(self, boards, moves):
        from numpy import array
        piece_map = {'P': 0, 'B': 8, 'N': 10, 'R': 12, 'Q': 14, 'K':15}
        piece_datapoints = list()
        board_datapoints = list()
        is_white = True
        for i, board in enumerate(boards):
            piece = boards[i][moves[i][0]]
            piece_datapoint = [0]*16
            piece_datapoint[piece_map[str(piece).upper()] + piece.ID - 1] = 1
            piece_datapoint = array(piece_datapoint)
            piece_datapoints.append(piece_datapoint)

            board_datapoint = [0]*16
            pieces = boards[i].white_pieces if is_white else boards[i].black_pieces
            for i in range(16):
                board_datapoint[i] = [0]*6
                board_datapoint[i] = array(board_datapoint[i])
            for piece in pieces:
                piece.compute_info(board)
                ID = piece.ID if piece.is_white is not None else 0
                value = piece.value if piece.is_white == is_white \
                        else piece.value * -1
                piece_info = [ID/10, value/10, piece.defends/10,
                        piece.threats/10, piece.threatens/10,
                        piece.num_moves/10]
                piece_info = array(piece_info)
                board_datapoint[piece_map[str(piece).upper()] + piece.ID - 1] = piece_info
            board_datapoint = array(board_datapoint)
            board_datapoint.reshape((1, 16, 6))
            board_datapoints.append(board_datapoint)
        return board_datapoints, piece_datapoints

    def _boards_to_datapoints(self, boards):
        from numpy import array
        is_white = True
        datapoints = []
        for board in boards:
            board_direction = range(8) if is_white else range(7, -1, -1)
            datapoint = []
            for row in board_direction:
                cur_row = []
                for column in range(8):
                    piece = board[column,row]
                    piece.compute_info(board)
                    ID = piece.ID if piece.is_white is not None else 0
                    value = piece.value if piece.is_white == is_white \
                            else piece.value * -1
                    dp = array([ID/10, value/10, piece.defends/10,
                        piece.threats/10, piece.threatens/10,
                        piece.num_moves/10])
                    cur_row.append(dp)
                cur_row = array(cur_row)
                datapoint.append(cur_row)
            is_white = not(is_white)
            datapoint = array(datapoint)
            datapoints.append(datapoint)
        datapoints = array(datapoints)
        datapoints = datapoints.reshape((datapoints.shape[0], 8, 8, 6))
        return datapoints

    def _move_to_datapoint(self, board, piece):
        from numpy import array
        datapoint = [0]*len(piece.move_IDs)
        for i, ID in enumerate(piece.move_IDs):
            piece_move = piece.move_IDs[ID](piece.location)
            piece_move = (piece_move//10, piece_move%10)
            if piece_move[0] >= 0 and piece_move[0] <= 7 \
                    and piece_move[1] >= 0 and piece_move[1] <= 7 \
                    and board.is_valid_move(piece, piece_move):
                datapoint[i] = 0.65
        return datapoint

