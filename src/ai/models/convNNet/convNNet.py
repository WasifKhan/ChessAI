'''
AI Implemented Using A Convolutional Neural Network
'''

from ai.models.base_ai import AI
import tensorflow as tf

class ConvNNet(AI):
    def __init__(self, location):
        super().__init__(location)

    def _build_model(self, game):
        from tensorflow.keras.models import Model
        from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Dense, Flatten
        from tensorflow.keras.optimizers import SGD
        from ai.data.data_extractor import DataExtractor
        self.data_extractor = DataExtractor(game)

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

    def _train_model(self, datapoints):
        from sklearn.model_selection import KFold
        from numpy import array
        self.scores, self.histories = list(), list()
        splits = 2
        kfold = KFold(splits, shuffle=True, random_state=1)
        for i in range(97):
            dataX, dataY = list(), list()
            for data in datapoints(self.location):
                board, move = data
                for i in range(len(board)):
                    dataX.append(board[i])
                    dataY.append(move[i])
            dataX, dataY = array(dataX), array(dataY)
            dataX = dataX.reshape((dataX.shape[0], 8, 8, 1))
            print(f'{i}%: Begin learning over {dataX.shape[0]} datapoints')
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
            print(f'{i}%: Done learning')
            self.model.save(f'{self.location}/brain.h5')

    def _evaluate_model(self):
        from matplotlib import pyplot
        from numpy import mean, std
        pyplot.title('Cross Entropy Loss')
        pyplot.plot(self.histories[-1].history['loss'], color='blue', label='train')
        pyplot.plot(self.histories[-1].history['val_loss'], color='orange', label='test')
        pyplot.show()
        print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(self.scores)*100, std(self.scores)*100, len(self.scores)))



