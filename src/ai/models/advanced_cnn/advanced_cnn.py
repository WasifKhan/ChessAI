'''
AI Implemented Using Basic Convolutional Neural Network

self._predict(board, is_white)
self._load_model()
self._build_model()
self._train_model()
self._evaluate_model()
self._move_to_datapoint(move)
self._board_to_datapoint(board, is_white)
'''

from ai.data.model_info import ModelInfo
from ai.models.cnn_basic.architecture import Architecture



class CnnBasic(ModelInfo):
    def __init__(self, game, location):
        super().__init__(game, location)
        self.model = Architecture(location)

    def _predict(self, board, is_white):
        from numpy import set_printoptions
        set_printoptions(suppress=True)
        piece_map = {0:'P', 1:'B', 2:'N', 3:'R', 4:'Q', 5:'K'}
        dp = self._boards_to_datapoints(board, is_white)
        model = self.model.get_model('S')
        prediction = model.predict(dp)[0].round(3)
        self.logger.debug(f'Piece probabilities: [P, B, N, R, Q, K]: {prediction}')
        for index in range(len(prediction)):
            if prediction[index] == max(prediction):
                break
        piece_model = self.model.get_model(piece_map[index])
        prediction = piece_model.predict(dp)[0].round(3)
        board_move = prediction.reshape((8,8))
        max_val = max(prediction.reshape((-1,)))
        piece_dp = dp[:,:,:,index:index+1].reshape((8,8))
        self.logger.debug(f'prediction:\n{board_move}')
        self.logger.debug(f'true:\n{piece_dp}')
        max_diff = None
        source = None
        board_direction = range(8) if is_white else range(7, -1, -1)
        found = False
        for row in board_direction and not Found:
            for column in range(8) and not Found:
                if board_move[row][column] == max_val:
                    destination = column*10 + 7-row
                    found = True
                    self.logger.debug(f'destination is: {destination}')
        for piece in board.white_pieces if is_white else board.black_pieces:
            if str(piece).upper() == piece_map[index] \
                    and board.is_valid_move(piece, (destination//10, destination%10)):
                source = piece.location[0]*10 + piece.location[1]
                self.logger.debug(f'source is: {source}')
                break
        self.logger.debug(f'Predicted {source} -> {destination}')
        if not source:
            return False
        return (source, destination)


    def _build_model(self):
        if self.model.built():
            return
        from tensorflow.keras.models import Model
        from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten
        self.logger.info('Building models')
        for ID in self.model.configurations:
            configuration = self.model.configurations[ID]
            layer_info, initializer, optimizer, loss_metric = configuration
            num_layers, density, supp_info, activation, = layer_info
            for piece in ['K', 'Q', 'R', 'N', 'B', 'P']:
                inputs = Input(shape=(8, 8, 6))
                x = inputs
                for i in range(num_layers):
                    x = Conv2D(density[i], supp_info[i],
                            activation[i], initializer)(x)
                x = Flatten()(x)
                outputs = Dense(64, 'softmax', initializer)(x)
                model = Model(inputs=inputs, outputs=outputs)
                model.compile(optimizer=optimizer, loss_metric[0], [loss_metric[1]])
                self.model.add_model(ID, piece, model)
            layer_info, initializer, optimizer, loss_metric = info
            num_layers, density, supp_info, activation, = layer_info
            inputs = Input(shape=(8, 8, 6))
            x = inputs
            for i in range(num_layers):
                x = Conv2D(density[i], supp_info[i],
                        activation[i], initializer)(x)
            x = Flatten()(x)
            outputs = Dense(6, 'softmax', initializer)(x)
            model = Model(inputs=inputs, outputs=outputs)
            model.compile(optimizer=optimizer, loss_metric[0], [loss_metric[1]])
            self.model.add_model(configuration, 'S', model)


    def _train_model(self):
        self.logger.info('Training models')
        for ID in self.models:
            self.logger.info(f'Training model:\n{ID}')
            for it in range(40):
                num_datapoints = 5000
                self.model.clear_data()
                self.logger.info(f'Begin downloading data: {i*10}% done')
                for i, data in enumerate(self.datapoints(num_datapoints),\
                        not(bool(it))):
                    if i >= 0 and i*100 % num_datapoints == 0:
                        self.logger.debug(f'{i*100//num_datapoints}% done downloading')
                    boards, moves = data
                    self._boards_to_datapoints(ID, boards, True, moves)
                self.model.prepare_model(ID)
                self.logger.info(f'Learning {ID} model')
                for tp in self.model.get_models(ID):
                    model, x, y, network = tp
                    performance = model.fit(x, y,
                            epochs=10, batch_size=512, validation_split=0.2, verbose=0)
                    self.model.add_performance(performance, ID, network)
                    self.model.save_model(ID)
            self.logger.info(f'Done learning')


    def _evaluate_model(self):
        from matplotlib import pyplot
        for performance in self.model.performances:
            fig, axs = pyplot.subplots(3, 2)
            fig.suptitle('Piece Networks')
            performances = iter(self.model.performances)
            sub_1 = False
            for i in range(3):
                for j in range(2):
                    network = next(performances)
                    if network == 'S':
                        sub_1 = True
                        continue
                    performance = self.model.performances[ID][network]
                    axs[i, j-sub_1].set_title(f'{phase} - {network}')
                    for perf in performance:
                        axs[i, j-sub_1].plot(perf.history['loss'], color='blue', label='Train Loss')
                        axs[i, j-sub_1].plot(perf.history['val_loss'], color='orange', label='Test Loss')
            for ax in axs.flat:
                ax.set(xlabel='Epoch', ylabel='Accuracy')
            for ax in axs.flat:
                ax.label_outer()
            fig_2, axs_2 = pyplot.subplots(3, 1)
            fig_2.suptitle('Selector Network')
            performance = self.model.performances[ID]['S']
            for perf in performance:
                axs_2.plot(perf.history['loss'], color='blue', label='Train Loss')
                axs_2.plot(perf.history['val_loss'], color='orange', label='Test Loss')
            pyplot.legend()
            pyplot.show()


    def _boards_to_datapoints(self, ID, boards, is_white=True, moves=None):
        from numpy import array
        piece_map = {'P':0, 'B':1, 'N':2, 'R':3, 'Q':4, 'K':5}
        if not moves:
            self.logger.debug('Begin prediction')
            board_direction = range(8) if is_white else range(7, -1, -1)
            x_data = []
            for row in board_direction:
                cur_row = []
                for column in range(8):
                    dp = [0]*6
                    if (piece := boards[column,row]).value != 0:
                        value = 1 if piece.is_white == is_white else -1
                        dp[piece_map[str(piece).upper()]] = value
                    cur_row.append(array(dp))
                x_data.append(array(cur_row))
            x_data = array(x_data)
            self.logger.debug('End prediction')
            x_data = x_data.reshape((1,8,8,6))
            return x_data

        self.logger.debug(f'Begin generating {len(boards)} datapoints')
        for i in range(len(boards)):
            board = boards[i]
            piece = boards[i][moves[i][0]]
            index = piece_map[str(piece).upper()]
            source = moves[i][0] if i % 2 == 0 else (moves[i][0]//10)*10 + (7-moves[i][0]%10)
            destination = moves[i][1] if i % 2 == 0 else (moves[i][1]//10)*10 + (7-moves[i][1]%10)
            move = (source, destination)
            board_direction = range(8) if i % 2 == 0 else range(7, -1, -1)
            x_data = []
            for row in board_direction:
                cur_row = []
                for column in range(8):
                    cur_piece = board[column,row]
                    dp = [0]*6
                    if str(cur_piece) != '.':
                        value = 1 if not(cur_piece.is_white) == i % 2 else -1
                        dp[piece_map[str(cur_piece).upper()]] = value
                    cur_row.append(dp)
                x_data.append(array(cur_row))
            x_data = array(x_data)
            y_selector = array([0]*6)
            y_selector[index] = 1
            y_piece = array([[0]*8]*8).reshape(8,8)
            y_piece[move[1]%10][move[1]//10] = 1
            y_piece = y_piece.reshape((-1, ))
            self.model.add_data(ID, 'S', x_data, y_selector)
            self.model.add_data(ID, str(piece).upper(), x_data, y_piece)
            is_white = not(is_white)

