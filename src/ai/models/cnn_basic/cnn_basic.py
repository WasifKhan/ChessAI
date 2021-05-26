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

        inputs = Input(shape=(64, 6))
        x = []
        for row in range(64):
            piece = Lambda(lambda x: x[row:row+1, 0:6])(inputs)
            piece = Conv1D(1, 6, activation='relu')(piece)
            x.append(piece)
        x = Concatenate()(x)
        x = Reshape((8,8,1))(x)
        x = Conv2D(32, (4, 4), activation='relu')(x)
        x = MaxPooling2D()(x)
        x = Flatten()(x)
        x = Dense(300, activation='relu')(x)
        outputs = Dense(142, activation='softmax')(x)
        opt = SGD(lr=0.05, momentum=0.9)
        model = Model(inputs, outputs)
        model.compile(optimizer=opt, loss='categorical_crossentropy',
                metrics=['accuracy'])
        self.model = model

    def _train_model(self):
        from sklearn.model_selection import train_test_split
        from numpy import array
        from time import time
        start = time()
        x_data, y_data = list(), list()
        print(f'Begin downloading data.')
        for i, data in enumerate(self.datapoints(30)):
            if i % 20 == 0:
                print(f'{i//20}% downloading')
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
        x_data = x_data.reshape((x_data.shape[0], 64, 6))
        x_train, x_test, y_train, y_test = \
                train_test_split(x_data, y_data, test_size = 0.2)
        print(f'Begin learning over {x_train.shape[0]} datapoints')
        self.performance = self.model.fit(x_train, y_train, epochs=5,
                batch_size=32, validation_data=(x_test, y_test), verbose=0)
        print(f'Done learning. Took {str(time()-start)[0:5]}s')
        self.model.save(f'{self.location}/brain.h5')


    def _evaluate_model(self):
        from matplotlib import pyplot
        from numpy import mean, std
        fig, axs = pyplot.subplots()
        axs.set_title('Cross Entropy Loss')
        axs.plot(self.performance.history['loss'], color='blue', label='train')
        axs.plot(self.performance.history['val_loss'], color='orange', label='test')
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
        datapoint = datapoint.reshape(1, 64, 6)
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
        print(prediction)
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

