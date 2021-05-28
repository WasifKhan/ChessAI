'''
AI Implemented Using A Basic Convolutional Neural Network
'''

from ai.models.base_model import BaseModel



class CnnBasic(BaseModel):
    def __init__(self, game, location):
        super().__init__(game, location)

    def _build_model(self):
        from tensorflow.keras.models import Model
        from tensorflow.keras.layers import Input, Conv1D, Conv2D, Dense, Flatten, \
            Concatenate, Lambda, Reshape, MaxPooling2D
        from tensorflow.keras.optimizers import SGD

        inputs = Input(shape=(8, 8, 6))
        x = Conv2D(32, (4, 4), activation='sigmoid')(inputs)
        x = Conv2D(16, (2, 2), activation='sigmoid')(x)
        x = Flatten()(x)
        x = Dense(200, activation='sigmoid')(x)
        outputs = Dense(142, activation='softmax')(x)
        opt = SGD(lr=0.05, momentum=0.9)
        model = Model(inputs, outputs)
        model.compile(optimizer=opt, loss='categorical_crossentropy',
                metrics=['categorical_accuracy'])
        self.model = model

    def _train_model(self):
        from sklearn.model_selection import train_test_split
        from numpy import array
        from time import time
        start = time()
        num_datapoints = 100
        x_data, y_data = list(), list()
        print(f'Begin downloading data.')
        for i, data in enumerate(self.datapoints(num_datapoints)):
            if i % (num_datapoints//100) == 0:
                print(f'{i//(num_datapoints//100)}% downloading')
            board, move = data
            self.game.__init__()
            for i in range(len(board)):
                x = self._board_to_datapoint(board[i], self.game.white_turn)
                self.game.move(*move[i])
                y = self._move_to_datapoint(self.game.board.move_ID)
                x_data.append(x)
                y_data.append(y)
        print(f'Done downloading. Took {time()-start}s')
        start = time()
        x_data, y_data = array(x_data), array(y_data)
        x_data = x_data.reshape((x_data.shape[0], 8, 8, 6))
        print(f'Begin learning over {x_train.shape[0]} datapoints')
        self.performance = self.model.fit(x_data, y_data, epochs=100, batch_size=32, validation_split=0.2)
        print(f'Done learning. Took {str(time()-start)[0:5]}s')
        self.model.save(f'{self.location}/brain.h5')


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

    def _move_to_datapoint(self, move):
        from ai.data.moves import MOVES
        from numpy import array
        datapoint = [0]*142
        datapoint[MOVES[move.upper()]] = 1
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

