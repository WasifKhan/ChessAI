'''
AI Implemented Using A Convolutional Neural Network
'''

from os import listdir
from ai.models.base_ai import AI
from numpy import mean
from numpy import array
from numpy import std
from matplotlib import pyplot
from sklearn.model_selection import KFold
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.models import load_model
from keras.models import save_model
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Flatten
from keras.optimizers import SGD


class ConvNNet(AI):
    def __init__(self, location):
        super().__init__(location)

    def _build_model(self):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(8, 8, 1)))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(300, activation='relu', kernel_initializer='he_uniform'))
        model.add(Dense(124, activation='softmax'))
        # compile model
        opt = SGD(lr=0.01, momentum=0.9)
        model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
        self.model = model

    def _train_model(self):
        self.scores, self.histories = list(), list()
        splits = 2 #CHANGE TO 5 when done
        kfold = KFold(splits, shuffle=True, random_state=1)
        # INCORRECT ATM
        dataX, dataY = list(), list()
        for i, data in enumerate(self._get_datapoint()):
            if i == 2:
                break
            [dataX.append(board) for board in data[0]]
            [dataY.append(move) for move in data[1]]
            i+= 1
        dataX, dataY = array(dataX), array(dataY)
        dataX = dataX.reshape((dataX.shape[0], 8, 8, 1))
        # enumerate splits
        i = 0
        for train_ix, test_ix in kfold.split(dataX):
            print(f'i is {i}')
            if i == 2:
                break
            i+= 1
            trainX, trainY, testX, testY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
            history = self.model.fit(trainX, trainY, epochs=2, batch_size=32, validation_data=(testX, testY), verbose=0)
            _, acc = self.model.evaluate(testX, testY, verbose=0)
            print('> %.3f' % (acc * 100.0))
            self.scores.append(acc)
            self.histories.append(history)
        self.model.save(f'{self.location}/brain.h5')

    def _evaluate_model(self):
        for i in range(len(self.histories)):
            # plot loss
            pyplot.subplot(2, 1, 1)
            pyplot.title('Cross Entropy Loss')
            pyplot.plot(self.histories[i].history['loss'], color='blue', label='train')
            pyplot.plot(self.histories[i].history['val_loss'], color='orange', label='test')
            # plot accuracy
            pyplot.subplot(2, 1, 2)
            pyplot.title('Classification Accuracy')
            pyplot.plot(self.histories[i].history['accuracy'], color='blue', label='train')
            pyplot.plot(self.histories[i].history['val_accuracy'], color='orange', label='test')
            pyplot.show()
        # print summary
        print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(self.scores)*100, std(self.scores)*100, len(self.scores)))
        # box and whisker plots of results
        pyplot.boxplot(self.scores)
        pyplot.show()

    def _load_model(self):
        return self.model.load_model(self.location + '/brain.h5')

