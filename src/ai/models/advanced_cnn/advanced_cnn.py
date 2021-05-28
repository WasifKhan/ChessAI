'''
AI Implemented Using Several Convolutional Neural Networks

models['should_move'] = list(queen_should_move, bishop_one_should_move, etc...) : x=board,y=move {0,1}
models['get_move'] = list(queen_get_move, bishop_one_get_move, etc...) : x=board, y=move ->{0,#moves}
models['vote_best_move'] = list(queen_vote, bishop_vote, etc...) : { {0,#moves} } -> move

'''

from ai.models.base_model import BaseModel



class AdvancedCnn(BaseModel):
    def __init__(self, game, location):
        super().__init__(game, location)

    def _build_model(self):
        from tensorflow.keras.models import Model
        from tensorflow.keras.layers import Input, Conv1D, Conv2D, Dense, Flatten, \
            Concatenate, Lambda, Reshape, MaxPooling2D
        from tensorflow.keras.optimizers import SGD
        self.game.__init__()
        self.models = dict()
        self.models['should_move'] = dict()
        self.models['get_move'] = dict()
        pieces = self.game.board.white_pieces
        for piece in pieces:
            inputs = Input(shape=(8, 8, 6))
            x = Conv2D(16, (4, 4), activation='relu')(inputs)
            x = Conv2D(8, (2, 2), activation='relu')(x)
            x = Flatten()(x)
            x = Dense(20, activation='sigmoid')(x)
            outputs = Dense(1, activation='sigmoid')(x)
            opt = SGD(lr=0.05, momentum=0.9)
            model = Model(inputs, outputs)
            model.compile(optimizer=opt, loss='binary_crossentropy',
                            metrics=['binary_accuracy'])
            self.models['should_move'][str(piece) + str(piece.ID)] = \
                    [model, None, None]

            inputs = Input(shape=(8, 8, 6))
            x = Conv2D(32, (4, 4), activation='relu')(inputs)
            x = Conv2D(16, (2, 2), activation='relu')(x)
            x = Flatten()(x)
            x = Dense(20, activation='sigmoid')(x)
            outputs = Dense(len(piece.move_IDs), activation='softmax')(x)
            opt = SGD(lr=0.05, momentum=0.9)
            model = Model(inputs, outputs)
            model.compile(optimizer=opt, loss='categorical_crossentropy',
                            metrics=['categorical_accuracy'])
            self.models['get_move'][str(piece) + str(piece.ID)] = \
                    [model, list(), list()]
        pieces = []
        inputs1 = Input(shape=(16,8))
        inputs2 = Input(shape(16,1))
        for i in range(16):
            x1 = Lambda(lambda x: x[i:i+1, :], output_shape=(8,))(inputs1)
            x1 = Dense(1, activation='ReLU')(x1)
            x2 = Lambda(lambda x: x[i:i+1], output_shape=(1,))(inputs2)
            x = Concatenate(x1, x2)
            pieces.append(x)
        x = Concatenate(pieces)
        x = Dense(30, activation='sigmoid')(x)
        outputs = Dense(16, activation='softmax')(x)
        model = Model(inputs=[inputs1, inputs2], outputs=outputs)
        model.compile(optimizer=opt, loss='categorical_crossentropy',
                        metrics=['categorical_accuracy'])

        self.models['vote_best_move'] = [model, list(list(), list()), list()]


    def _train_model(self):
        from sklearn.model_selection import train_test_split
        from numpy import array
        from time import time
        start = time()
        num_datapoints = 100
        x_data, y_data = dict(), dict()
        print(f'Begin downloading data.')
        for i, data in enumerate(self.datapoints(num_datapoints)):
            if i % (num_datapoints//100) == 0:
                print(f'{i//(num_datapoints//100)}% downloading')
            boards, moves = data
            self.game.__init__()
            for i in range(len(boards)):
                my_pieces = boards[i].white_pieces if self.game.white_turn \
                        else boards[i].black_pieces
                piece = boards[i][moves[i][0]]
                x = self._board_to_datapoint(boards[i], self.game.white_turn)
                self.game.move(*moves[i])
                for key in self.models['should_move']:
                    self.models['should_move'][key][1].append(x)
                    self.models['should_move'][key][2].append(1) \
                        if key == str(piece) + str(piece.ID) else 0
                y = self._move_to_datapoint(self.game.board.move_ID, piece)
                self.models['get_move'][str(piece) + str(piece.ID)][1].append(x)
                self.models['get_move'][str(piece) + str(piece.ID)][2].append(y)
                x = self._pieces_to_datapoint(my_pieces)
                y = self._piece_to_datapoint(piece)
                self.models['vote_best_move'][1][0].append(x)
                self.models['vote_best_move'][2].append(y)
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
        print(f'Begin learning over {x_train.shape[0]} datapoints')
        self.performance = self.model.fit(x_data, y_data, epochs=100, batch_size=32, validation_split=0.2)
        print(f'Done learning. Took {str(time()-start)[0:5]}s')

        '''
        Populate self.models['vote_best_move'][1][1] with predictions from
        'get_move' and 'should_move'
        make all lists in self.models['vote_best_move'] numpy arrays
        train vote_best_model
        '''
        #self.model.save(f'{self.location}/brain.h5')


    def _evaluate_model(self):
        from matplotlib import pyplot
        from numpy import mean, std
        fig, axs = pyplot.subplots()
        axs.set_title('Prediction Accuracy')
        axs.xlabel('Epoch')
        axs.ylabel('Accuracy')
        axs.plot(self.performance.history['categorical_accuracy'], color='blue', label='train')
        axs.plot(self.performance.history['val_categorical_accuracy'], color='orange', label='test')
        pyplot.legend()
        pyplot.show()

    def _pieces_to_datapoint(self, pieces):
        pass

    def _piece_to_datapoint(self, piece):
        pass

    def _board_to_datapoint(self, board, is_white):
        from numpy import array
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
                cur_row.append([ID, value, piece.defends, piece.threats,
                            piece.threatens, piece.num_moves])
            datapoint.append(cur_row)
        datapoint = array(datapoint)
        datapoint = datapoint.reshape(1, 8, 8, 6)
        return datapoint

    def _move_to_datapoint(self, move, piece):
        from numpy import array
        datapoint = [0]*len(piece.move_IDs)
        datapoint[int(move[-1]] = 1
        datapoint = array(datapoint)
        return datapoint

    def _prediction_to_move(self, prediction, board, is_white):
        from ai.data.moves import MOVES
        for i, val in enumerate(prediction[0]):
            if val == max(prediction[0]):
                prediction = i
                break
        for key in MOVES:
            if MOVES[key] == prediction:
                move = key
        my_piece, ID, move_ID = move[0], int(move[1]), move[2:]
        my_piece = my_piece if is_white else my_piece.lower()
        pieces = board.white_pieces if is_white else board.black_pieces
        for piece in pieces:
            if str(piece) == str(my_piece) and piece.ID == ID:
                return piece.get_move(int(move_ID))

