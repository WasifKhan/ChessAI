'''
AI Implemented Using A Convolutional Neural Network
'''

from ai.models.base_model import BaseModel



class CnnBasic(BaseModel):
    def __init__(self, game, location):
        super().__init__(game, location)

    def _build_model(self):
        from tensorflow.keras.models import Model
        from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Dense, Flatten
        from tensorflow.keras.optimizers import SGD

        board = Input(shape=(8, 8, 1))
        layer_1 = Conv2D(16, (3, 3), activation='sigmoid', kernel_initializer='he_uniform')(board)
        layer_2 = MaxPooling2D((2, 2))(layer_1)
        layer_3 = Flatten()(layer_2)
        output = Dense(142, activation='softmax')(layer_3)
        opt = SGD(lr=0.05, momentum=0.75)
        model = Model(board, output)
        model.compile(optimizer=opt, loss='categorical_crossentropy',
                metrics=['accuracy'])
        self.model = model

    def _train_model(self):
        from sklearn.model_selection import KFold
        from numpy import array
        dataX, dataY = list(), list()
        for i, data in enumerate(self.datapoints(100)):
            print(f'{i}% done downloading')
            board, move = data
            self.game.__init__()
            for i in range(len(board)):
                x = self._board_to_datapoint(board[i], self.game.white_turn)
                self.game.move(*move[i])
                y = self._move_to_datapoint(self.game.board.move_ID)
                dataX.append(x)
                dataY.append(y)
        dataX, dataY = array(dataX), array(dataY)
        dataX = dataX.reshape((dataX.shape[0], 8, 8, 1))
        print(f'Begin learning over {dataX.shape[0]} datapoints')
        self.scores, self.histories = list(), list()
        splits = 5
        kfold = KFold(splits, shuffle=True, random_state=1)
        for i, train_test in enumerate(kfold.split(dataX)):
            train_ix, test_ix = train_test
            trainX, trainY, testX, testY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
            history = self.model.fit(trainX, trainY, epochs=10, batch_size=32,
                    validation_data=(testX, testY), verbose=0)
            _, acc = self.model.evaluate(testX, testY, verbose=0)
            print(f'Learning {i}/{splits} accuracy: {str(acc*100)[0:5]}')
            self.scores.append(acc)
            self.histories.append(history)
        self.scores.append(acc)
        self.histories.append(history)
        print(f'Done learning')
        self.model.save(f'{self.location}/brain.h5')

    def _evaluate_model(self):
        from matplotlib import pyplot
        from numpy import mean, std
        pyplot.title('Cross Entropy Loss')
        pyplot.plot(self.histories[-1].history['loss'], color='blue', label='train')
        pyplot.plot(self.histories[-1].history['val_loss'], color='orange', label='test')
        pyplot.show()
        print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(self.scores)*100, std(self.scores)*100, len(self.scores)))


    def _board_to_datapoint(self, board, is_white):
        from numpy import array
        piece_mapping = {'P': 1.0, 'B': 3.2, 'N' : 3.1, 'R': 5.0, 'Q': 9.0, 'K': 100.0}
        board_direction = range(8) if is_white else range(7, -1, -1)
        datapoint = [[0 if (piece := board[column,row]).is_white == None \
                        else piece_mapping[str(piece).upper()] \
                        if piece.value == 9  and piece.is_white == is_white \
                        else piece_mapping[str(piece).upper()] * - 1 \
                        if piece.value == 9 \
                        else piece_mapping[str(piece).upper()] + piece.ID/100 \
                        if piece.is_white == is_white \
                        else (piece_mapping[str(piece).upper()] + piece.ID/100) * -1
                    for column in range(8)] \
                    for row in board_direction]
        datapoint = array(datapoint)
        datapoint = datapoint.reshape(1, 8, 8, 1)
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

