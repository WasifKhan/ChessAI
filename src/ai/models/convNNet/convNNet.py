'''
AI Implemented Using A Convolutional Neural Network
'''

from ai.models.base_ai import AI
import tensorflow as tf

class ConvNNet(AI):
    def __init__(self, location):
        super().__init__(location)

    '''
    This is impossible due to Eager Execution over Graph Execution
    Don't really want to do graph execution due to other methods slowing down
    '''
    def board_loss(self, board):
        # NEED TO CONVERT BOARD FROM KerasTensor->List
        def loss(y_true, y_pred):
            mae = MeanAbsoluteError()
            true_losses = []
            predicted_losses = []
            for i in range(len(y_true)):
                true_board = self.data_extractor._datapoint_to_board(board)
                pred_board = self.data_extractor._datapoint_to_board(board)
                true_move = self.data_extractor._prediction_to_move(y_true, true_board, True)
                pred_move = self.data_extractor._prediction_to_move(y_pred, pred_board, True)
                true_board.move(*true_move)
                pred_board.move(*pred_move)
                true_losses.append(true_board.value)
                pred_losses.append(pred_board.value)
            return mae(pred_losses, true_losses).numpy()
        return loss

    def _build_model(self, game):
        from tensorflow.keras.models import Model
        from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Dense, Flatten
        from tensorflow.keras.optimizers import SGD
        from tensorflow.keras.losses import MeanSquaredError
        from ai.data.data_extractor import DataExtractor
        self.data_extractor = DataExtractor(game)

        board = Input(shape=(8, 8, 1))
        layer_1 = Conv2D(3, (3, 3), activation='sigmoid', kernel_initializer='he_uniform')(board)
        layer_2 = MaxPooling2D((2, 2))(layer_1)
        layer_3 = Flatten()(layer_2)
        output = Dense(142, activation='sigmoid')(layer_3)
        opt = SGD(lr=0.01, momentum=0.9)
        model = Model(board, output)
        # Try with loss=binarycrossentropy + categoriccalcrossentropy
        model.compile(optimizer=opt, loss=MeanSquaredError(),
                metrics=['accuracy'])
        self.model = model

    def _train_model(self, datapoints):
        from sklearn.model_selection import KFold
        from numpy import array
        self.scores, self.histories = list(), list()
        splits = 4
        kfold = KFold(splits, shuffle=True, random_state=1)
        dataX, dataY = list(), list()
        for data in datapoints:
            board, move = data
            for i in range(len(board)):
                dataX.append(board[i])
                dataY.append(move[i])
        dataX, dataY = array(dataX), array(dataY)
        dataX = dataX.reshape((dataX.shape[0], 8, 8, 1))
        print('Begin learning')
        for i, train_test in enumerate(kfold.split(dataX)):
            train_ix, test_ix = train_test
            trainX, trainY, testX, testY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
            history = self.model.fit(trainX, trainY, epochs=5, batch_size=32, verbose=1)
            _, acc = self.model.evaluate(testX, testY, verbose=1)
            print(f'Learning {i}/{splits} accuracy: {str(acc*100)[0:5]}')
            self.scores.append(acc)
            self.histories.append(history)
        self.scores.append(acc)
        self.histories.append(history)
        print('Done learning')
        self.model.save(f'{self.location}/brain.h5')

    def _evaluate_model(self):
        from matplotlib import pyplot
        from numpy import mean, std
        pyplot.title('Classification Accuracy')
        pyplot.plot(self.histories[-1].history['accuracy'], color='blue', label='train')
        pyplot.show()
        print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(self.scores)*100, std(self.scores)*100, len(self.scores)))
