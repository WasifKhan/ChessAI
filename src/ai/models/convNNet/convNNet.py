'''
AI Implemented Using A Convolutional Neural Network
'''

from ai.models.base_ai import AI
from numpy import array


class ConvNNet(AI):
    def __init__(self, location):
        super().__init__(location)

    def _build_model(self):
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
        from tensorflow.keras.optimizers import SGD
        model = Sequential()
        model.add(Conv2D(3, (3, 3), activation='sigmoid', kernel_initializer='he_uniform', input_shape=(8, 8, 1)))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(142, activation='softmax'))
        # compile model
        opt = SGD(lr=0.01, momentum=0.9)
        model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
        self.model = model

    def _train_model(self, datapoints):
        from ai.data.data_extractor import DataExtractor
        from sklearn.model_selection import KFold
        self.scores, self.histories = list(), list()
        splits = 4
        kfold = KFold(splits, shuffle=True, random_state=1)
        dataX, dataY = list(), list()
        for data in datapoints:
            [dataX.append(board) for board in data[0]]
            [dataY.append(move) for move in data[1]]
        dataX, dataY = array(dataX), array(dataY)
        dataX = dataX.reshape((dataX.shape[0], 8, 8, 1))
        print('Begin learning')
        # enumerate splits
        for i, train_test in enumerate(kfold.split(dataX)):
            train_ix, test_ix = train_test
            trainX, trainY, testX, testY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
            history = self.model.fit(trainX, trainY, epochs=5, batch_size=32, validation_data=(testX, testY), verbose=0)
            _, acc = self.model.evaluate(testX, testY, verbose=0)
            print(f'Learning {i}/{splits} accuracy: {str(acc*100)[0:5]}')
            self.scores.append(acc)
            self.histories.append(history)
        print('Done learning')
        self.model.save(f'{self.location}/brain.h5')

    def _evaluate_model(self):
        from matplotlib import pyplot
        from numpy import mean, std
        pyplot.title('Classification Accuracy')
        pyplot.plot(self.histories[-1].history['accuracy'], color='blue', label='train')
        pyplot.plot(self.histories[-1].history['val_accuracy'], color='orange', label='test')
        pyplot.show()
        print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(self.scores)*100, std(self.scores)*100, len(self.scores)))
